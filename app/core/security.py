from app.core.config import settings
from flaat.fastapi import Flaat

flaat = Flaat()
flaat.set_trusted_OP_list([str(x) for x in settings.TRUSTED_OP_LIST])
