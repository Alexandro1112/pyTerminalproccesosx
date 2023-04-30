import objc
import subprocess
from .exceptions import *

class BlueTooth(object):
    def __init__(self):
        bundle_path = '/System/Library/Frameworks/IOBluetooth.framework'

        dir(objc.loadBundle(objc.infoForFramework(bundle_path)[1], bundle_path=bundle_path,
                            module_globals=globals()))

        self.bluetooth = subprocess.getoutput(cmd='system_profiler SPBluetoothDataType')

        devices = globals()['IOBluetoothDevice']  # Ignore error.IOBluetoothDevice not objective-class,
        # and when I pack him in objc.loadBundle I
        # got error, tied with subcridiable.
        address = devices.recentDevices_(0)

        for Query_Devises in address:
            self.device = Query_Devises

    def get_paired_devices(self):
        return (self.device.getNameOrAddress())

    def isEnable(self):
        return globals()['IOBluetoothPreferenceGetControllerPowerState']() != 0

    def set_bluetooth_by_enable(self):
        globals()['IOBluetoothPreferenceSetControllerPowerState'](1)

    def set_bluetooth_by_disable(self):
        globals()['IOBluetoothPreferenceSetControllerPowerState'](0)

    def get_all_address(self):
        """[0] or [1]"""
        ADDRESID = subprocess.getoutput(cmd='system_profiler SPBluetoothDataType | grep Address').split('Address')[1:]
        ADDRESID = set(ADDRESID)
        for ID in ADDRESID:
            yield ID.rstrip().replace(': ', '').lstrip()

    def pair_to_devise(self, address, duration_pair):
        try:
            device = globals()['IOBluetoothDevice'].withAddressString_(address)
            device.openConnection()
            device.openConnection_withPageTimeout_authenticationRequired_(None, duration_pair, False)
        except AttributeError:
            raise BluetoothConnectionError(f'Can not connect to devise, with address {repr(address)}')


