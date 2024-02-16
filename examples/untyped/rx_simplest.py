# fmt: off
import mwings as mw
twelite = mw.Twelite(mw.utils.ask_user_for_port())
@twelite.on(mw.common.PacketType.APP_TWELITE)
def on_app_twelite(packet):
    print(packet.to_json())
twelite.start()  # Caution: creates an orphan thread
# fmt: on
