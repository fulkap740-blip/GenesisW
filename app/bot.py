from app.handlers_user import *
from app.handlers_admin import *

dp.message.register(start, F.text == "/start")
dp.callback_query.register(profile, F.data == "profile")
dp.callback_query.register(new_request, F.data == "new_request")
dp.callback_query.register(choose_offer, F.data.startswith("offer_"))
dp.message.register(save_wallet, F.text.startswith("T"))
dp.message.register(step_video, RequestForm.video)
dp.message.register(step_proof, RequestForm.proof)
dp.message.register(step_views, RequestForm.views)
dp.callback_query.register(send_today, F.data == "send_today")
dp.callback_query.register(help_cmd, F.data == "help")
dp.callback_query.register(back, F.data == "back")

dp.message.register(gen_admin, F.text.startswith("/gen_admin"))
dp.message.register(exit_admin, F.text == "/exit")
dp.callback_query.register(admin_today, F.data == "admin_today")