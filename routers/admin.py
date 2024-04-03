from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import config
import keyboards
from states.AdminChangeStates import AdminChangeStates
import json

router = Router()


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if config.ADMIN_ID == message.chat.id:
        await message.answer("Здравствуй, админ", reply_markup=keyboards.admin())


@router.callback_query(F.data == "change_hello")
async def change_hello(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Отправьте новое приветственное сообщение")
    await state.set_state(AdminChangeStates.hello_message_change)


@router.message(AdminChangeStates.hello_message_change)
async def get_hello_message(message: Message, state: FSMContext):
    file_id = None
    caption = None

    if message.video:
        file_id = message.video.file_id

    if message.caption:
        caption = message.caption

    if message.text:
        caption = message.text

    data: dict = json.loads(open("admin_settings.json", "rb").read().decode())
    data.update({"file_id": file_id or data["file_id"], "caption": caption or data["caption"]})
    json.dump(data, open("admin_settings.json", "w"))

    await state.clear()
    await message.answer("Приветственное сообщение было изменено!", reply_markup=keyboards.admin())


@router.callback_query(F.data == "change_invite")
async def change_invite(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Напиши новую ссылку")
    await state.set_state(AdminChangeStates.change_invite)


@router.message(AdminChangeStates.change_invite)
async def change_invite(message: Message, state: FSMContext):
    if (not message.text) or not ("http://" in message.text or "https://" in message.text):
        return await message.answer("Напишие пожалуйста ссылку текстом :(")

    data: dict = json.loads(open("admin_settings.json", "rb").read().decode())
    data.update({"url": message.text})
    json.dump(data, open("admin_settings.json", "w"))

    await state.clear()
    await message.answer("Ссылка изменена")
