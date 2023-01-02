import logging
import bluezero.adapter
import bluezero.broadcaster
import bluezero.peripheral

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s %(message)s', level=logging.DEBUG)


# Dev name D110-E623022657
# advertising 0000: 0x23e60276b81d   # first six are serial? perhaps remaineder is printer or crc or something?

NIM_S1 = "49535343-fe7d-4ae5-8fa9-9fafd205e455"
NIM_S1_C1 = "49535343-1e4d-4bd9-ba61-23c646249616" # notify,read  # Reads 20 bytes?
NIM_S1_C2 = "49535343-8841-43f4-a8d4-ecbe34729bb3" # write
NIM_S1_C3 = "49535343-6daa-4d02-abf6-19569aca69fe" # write no response
NIM_S1_C4 = "49535343-aca3-481c-91ec-d85e28a60318" # notify, read, write # reads 20 bytes?
NIM_S2 = "e7810a71-73ae-499d-8c15-faa9aef0c3f2"
NIM_S2_C1 = "bef8d6c9-9c21-4c9e-b632-bd58c1009f9f" # notify, read, write no response (reads 1 byte)

def main_beacon():
    alt = bluezero.broadcaster.Beacon()
    alt.add_manufacturer_data(
        '0000',
        b'\x23\xe6\x02\x76\xb8\x1d')

    alt.start_beacon()


def read_debug1():
    print("READ1?!")
    return b'\0'

def read_debug20():
    print("READ20?!")
    return b'\0' * 20

def write_debug(value, options):
    print("write?", value, options)

def notify_debug(notifying, char):
    print("notify?", notifying, char)

def main():
    logger = logging.getLogger('kkk')
    logger.setLevel(logging.DEBUG)

    adapter_address = list(bluezero.adapter.Adapter.available())[0].address
    # Create peripheral
    logger.debug("Creating periph on adapter: %s", adapter_address)
    # 4C:1D:96:DC:12:92
    #ln = 'D110-4242426969'
    #manud = bytearray([0x42, 0x42, 0x42, 0x69, 0x69])
    ln="D110-1D4C960000"
    manud = bytearray([0x4c, 0x1d, 0x96, 0xdc, 0x12, 0x92])

    # This is the real one, with a mac of 23:e6:02:76:b8:1d
    #ln = "D110-E623022657"
    #manud = bytearray([0x23, 0xe6, 0x02, 0x76, 0xb8, 0x1d])
    nim = bluezero.peripheral.Peripheral(adapter_address,
                                       local_name=ln)
    nim.advert.manufacturer_data(0, manud)

    nim.add_service(srv_id=1, uuid=NIM_S1, primary=True)
    nim.add_characteristic(srv_id=1, chr_id=1, uuid=NIM_S1_C1,
                           value=[], notifying=False,
                           flags=['read', 'notify'],
                           read_callback=read_debug1,
                           write_callback=None,
                           notify_callback=notify_debug,
                           )
    nim.add_characteristic(srv_id=1, chr_id=2, uuid=NIM_S1_C2,
                           value=[], notifying=False,
                           flags=['write'],
                           read_callback=None,
                           write_callback=write_debug,
                           notify_callback=None,
                           )
    nim.add_characteristic(srv_id=1, chr_id=3, uuid=NIM_S1_C3,
                           value=[], notifying=False,
                           flags=['write-without-response'],
                           read_callback=None,
                           write_callback=write_debug,
                           notify_callback=None,
                           )
    nim.add_characteristic(srv_id=1, chr_id=4, uuid=NIM_S1_C4,
                           value=[], notifying=False,
                           flags=['notify', 'read', 'write'],
                           read_callback=read_debug20,
                           write_callback=write_debug,
                           notify_callback=notify_debug,
                           )

    #nim.add_service(srv_id=2, uuid=NIM_S2, primary=True)
    #nim.add_characteristic(srv_id=2, chr_id=1, uuid=NIM_S2_C1,
    #                       value=[], notifying=False,
    #                       flags=['read', 'notify', 'write-no-response'],
    #                       read_callback=read_debug20,
    #                       write_callback=write_debug,
    #                       notify_callback=None,
    #                       )


    nim.publish()

if __name__ == '__main__':
    main()
