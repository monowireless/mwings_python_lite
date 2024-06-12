# fmt: off
import mwingslite as mw
twelite = mw.Twelite("/dev/ttyS0") # For RasPi (serial0)
# twelite = mw.Twelite("/dev/ttyUSB0") # For RasPi (USB)
@twelite.on(mw.common.PacketType.APP_TWELITE)
def on_app_twelite(packet):
    print(packet.to_json())
twelite.start()  # Caution: creates an orphan thread
# fmt: on
