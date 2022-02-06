import json


def get_data(file):
    """
    Получает данные из json файла.
    :param file: файл с данными.
    :return:  данные в json формате.
    """
    with open(file, 'r', encoding='UTF-8') as f:
        return json.load(f)


def convert_user_to_dict(user):
    """
    Преобразует данные пользователя в словарь.
    :param user: экземпляр User.
    :return: словарь с данными.
    """
    return {"id": user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'email': user.email,
            'role': user.role,
            'phone': user.phone
            }


def convert_order_to_dict(order):
    """
    Преобразует данные заказа в словарь.
    :param order: экземпляр Order.
    :return: словарь с данными.
    """
    return {"id": order.id,
            'name': order.name,
            'description': order.description,
            'start_date': order.start_date,
            'end_date': order.end_date,
            'address': order.address,
            'price': order.price,
            'customer_id': order.customer_id,
            'executor_id': order.executor_id
            }


def convert_offer_to_dict(offer):
    """
    Преобразует данные предложения в словарь.
    :param offer: экземпляр Offer.
    :return: словарь с данными.
    """
    return {"id": offer.id,
            'order_id': offer.order_id,
            'executor_id': offer.executor_id
            }
