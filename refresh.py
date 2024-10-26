import asyncio
from datetime import datetime
from database.models import Problems
from database.models import Person
from database.models import Type
from use_email import Email


async def main():
    problems = await Problems.all().values()
    list_peoples_for_problem = []
    list_emails_for_problem = []
    professional_name = ""
    for element in problems:
        if element['type_id'] is not None:
            professional = list(await Type.filter(id=element['type_id']).values())[0].get('id')
            professional_name = str(list(await Type.filter(id=element['type_id']).values())[0].get('full_name'))
            if list(await Person.filter(id=professional).values())[0] not in list_peoples_for_problem:
                list_peoples_for_problem.append(list(await Person.filter(id=professional).values())[0])
    for element in list_peoples_for_problem:
        list_emails_for_problem.append(element.get("email"))
    last_time = datetime.now()
    while True:
        lst_update = []
        data = await Problems.all()
        for val in data:
            check_time = val.time.replace(tzinfo=None)
            if check_time > last_time:
                lst_update.append(val)

        if lst_update:
            for receiver_email in list_emails_for_problem:
                for element in lst_update:
                    priority = element.priority.replace('PriorityEnum.', '').replace('StatusEnum.', "")
                    description = element.description
                    message = element.message
                    status = element.status
                    time = element.time

                    new_email = Email(
                        priority=priority,
                        description=description,
                        message=message,
                        status=status,
                        type=professional_name,
                        # тут должна была быть колонка с author (автор проблемы тот, кто заметил проблему)
                        receiver_email=receiver_email,
                        time=time
                    )
                    new_email.send_new_email()
        last_time = datetime.now()
        await asyncio.sleep(15)


async def setup():
    await main()


# import asyncio
# from time import sleep
# from datetime import datetime
# from database.models import Problems
# from .aiog import bot
#
#
# async def main():
#     last_time = datetime.now()
#     while True:
#
#         lst_update = []
#         data = await Problems.all()
#         for val in data:
#             check_time = val.time.replace(tzinfo=None)
#
#             if (check_time > last_time):
#                 lst_update.append(val)
#
#         if lst_update != []:
#             from .aiog import users
#             for i in lst_update:
#                 id = i.id
#                 priority = i.priority.replace('PriorityEnum.', '')
#                 description = i.description
#                 message = i.message
#
#                 for g in users:
#                     await bot.send_message(g,
#                                            f'❗<b>ВНИМАНИЕ</b> ПРОБЛЕМА❗:\n\n<b>Id: {id}</b> Тип проблемы: <b>{priority}</b>\nОписание: {description}\nСообщение:{message}',
#                                            parse_mode='html')
#
#         last_time = datetime.now()
#         await asyncio.sleep(15)
#
#
# async def setup():
#     await main()








