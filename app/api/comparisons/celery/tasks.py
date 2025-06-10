from app.api.comparisons.celery.celery_app import celery
from app.api.comparisons.commands.comparison_crud import get_all_products_with_parsing_sync, update_product_parsing_sync
from parsing.all_parsing import KaspiParser
from database.db import SessioLocal
import logging
from utils.context_utils import decrypt_password
from datetime import datetime


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@celery.task
def parse_kaspi_products():
    def run_parser():
        with SessioLocal() as db:
            logger.info("Получение продуктов из базы данных")
            seller_products = get_all_products_with_parsing_sync(db)
            
            seller_products_map = {}
            for sp in seller_products:
                seller_id = sp.seller_id
                if seller_id not in seller_products_map:
                    decrypted_password = decrypt_password(sp.seller.kaspi_password)
                    seller_products_map[seller_id] = {
                        'kaspi_email': sp.seller.kaspi_email,
                        'kaspi_password': decrypted_password,
                        'products': []
                    }
                product_dict = {
                    'product_id': sp.product.id,
                    'vender_code': sp.product.vender_code,
                    'min_price': sp.product.product_comparisons[0].min_price if sp.product.product_comparisons else None,
                    'max_price': sp.product.product_comparisons[0].max_price if sp.product.product_comparisons else None,
                    'step': sp.product.product_comparisons[0].step if sp.product.product_comparisons else None,
                    'market_link': sp.product.market_link
                }
                if all([product_dict['min_price'], product_dict['max_price'], product_dict['step'], product_dict['market_link']]):
                    seller_products_map[seller_id]['products'].append(product_dict)
                else:
                    logger.warning(f"Пропуск продукта {sp.product.vender_code}: отсутствуют необходимые данные")

            results = []
            parser = KaspiParser()
            for seller_id, seller_data in seller_products_map.items():
                result = parser.run(
                    products=seller_data['products'],
                    kaspi_email=seller_data['kaspi_email'],
                    kaspi_password=seller_data['kaspi_password']
                )
                if isinstance(result, tuple) and len(result) == 3:
                    updated_prices, updated_first_market, updated_price_first_market = result
                    update_data = {}
                    for price_item in updated_prices:
                        if 'product_id' in price_item and 'new_price' in price_item:
                            update_data[price_item['product_id']] = {
                                'new_price': price_item['new_price']
                            }
                    for fm_item in updated_first_market:
                        if 'product_id' in fm_item and 'first_market' in fm_item:
                            update_data.setdefault(fm_item['product_id'], {}).update({
                                'first_market': fm_item['first_market']
                            })
                    for pfm_item in updated_price_first_market:
                        if 'product_id' in pfm_item and 'price_first_market' in pfm_item:
                            update_data.setdefault(pfm_item['product_id'], {}).update({
                                'price_first_market': pfm_item['price_first_market']
                            })
                    for product_id, data in update_data.items():
                        try:
                            update_product_parsing_sync(
                                product_id=product_id,
                                product_data={
                                    'price': data['new_price'],
                                    'first_market': data.get('first_market', None),
                                    'price_first_market': data.get('price_first_market', None),
                                    'updated_at': datetime.utcnow()
                                },
                                db=db
                            )
                            logger.info(f"Обновлена цена для продукта ID {product_id} до {data['new_price']}")
                        except Exception as e:
                            logger.error(f"Ошибка обновления продукта ID {product_id}: {str(e)}")
                results.append(result)

            return results

    try:
        logger.info("Запуск задачи parse_kaspi_products")
        return run_parser()
    except Exception as e:
        logger.error(f"Ошибка выполнения задачи parse_kaspi_products: {str(e)}")
        raise