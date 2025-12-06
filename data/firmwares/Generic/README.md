

URL the Project: [MicroPython - Python for microcontrollers](https://micropython.org/download/ESP32_GENERIC_S3/)





## ESP32-S3

![](https://micropython.org/resources/micropython-media/boards/ESP32_GENERIC_S3/generic_s3.jpg)

**Vendor:** Espressif

**Features:** BLE, External Flash, External RAM, WiFi

**Source on GitHub:** [esp32/ESP32_GENERIC_S3](https://github.com/micropython/micropython/tree/master/ports/esp32/boards/ESP32_GENERIC_S3)

**More info:** [Website](https://www.espressif.com/en/products/modules)

The following files are firmware that should work on most ESP32-S3-based
boards with 4MiB or more of flash, including WROOM and MINI modules.

This firmware supports configurations with and without SPIRAM (also known as
PSRAM) and will auto-detect a connected SPIRAM chip at startup and allocate
the MicroPython heap accordingly. However if your board has Octal SPIRAM, then
use the "spiram-oct" variant.

## Installation instructions

Program your board using the esptool.py program, found [here](https://docs.espressif.com/projects/esptool/en/latest/esp32s3/).

*Windows users:* You may find the installed program is called `esptool` instead of `esptool.py`.

### Erasing

If you are putting MicroPython on your board for the first time then you should
first erase the entire flash using:

```bash
esptool.py erase_flash
```

`esptool.py` will try to detect the serial port with the ESP32 automatically,
but if this fails or there might be more than one Espressif-based device
attached to your computer then pass the `--port` option with the name of the
target serial port. For example:

```bash
esptool.py --port PORTNAME erase_flash
```

- On Linux, the port name is usually similar to `/dev/ttyUSB` or `/dev/ttyACM0`.
- On Mac, the port name is usually similar to `/dev/cu.usbmodem01`.
- On Windows, the port name is usually similar to `COM4`.

### Flashing

Then deploy the firmware to the board, starting at address 0:

```bash
esptool.py --baud 460800 write_flash 0 ESP32_BOARD_NAME-DATE-VERSION.bin
```

Replace `ESP32_BOARD_NAME-DATE-VERSION.bin` with the `.bin` file downloaded from this page.

As above, if `esptool.py` can't automatically detect the serial port
then you can pass it explicitly on the command line instead. For example:

```bash
esptool.py --port PORTNAME --baud 460800 write_flash 0 ESP32_BOARD_NAME-DATE-VERSION.bin
```

### Troubleshooting

If flashing starts and then fails partway through, try removing the `--baud 460800` option to flash at the slower default speed.

If these steps don't work, consult the [MicroPython ESP32 Troubleshooting
steps](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html#troubleshooting-installation-problems) and the [esptool
documentation](https://docs.espressif.com/projects/esptool/en/latest/esp32s3/esptool/basic-options.html).

**Important**: From the options below, download the `.bin` file for your board.

## Firmware

### Releases

**[v1.26.1 (2025-09-11) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20250911-v1.26.1.uf2)** 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20250911-v1.26.1.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20250911-v1.26.1.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20250911-v1.26.1.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20250911-v1.26.1.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.26.1) 
(latest)

[v1.26.0 (2025-08-09) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20250809-v1.26.0.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20250809-v1.26.0.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20250809-v1.26.0.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20250809-v1.26.0.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20250809-v1.26.0.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.26.0)

[v1.25.0 (2025-04-15) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20250415-v1.25.0.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20250415-v1.25.0.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20250415-v1.25.0.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20250415-v1.25.0.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20250415-v1.25.0.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.25.0)

[v1.24.1 (2024-11-29) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20241129-v1.24.1.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20241129-v1.24.1.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20241129-v1.24.1.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20241129-v1.24.1.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20241129-v1.24.1.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.24.1)

[v1.24.0 (2024-10-25) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20241025-v1.24.0.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20241025-v1.24.0.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20241025-v1.24.0.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20241025-v1.24.0.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20241025-v1.24.0.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.24.0)

[v1.23.0 (2024-06-02) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20240602-v1.23.0.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20240602-v1.23.0.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20240602-v1.23.0.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20240602-v1.23.0.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20240602-v1.23.0.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.23.0)

[v1.22.2 (2024-02-22) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20240222-v1.22.2.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20240222-v1.22.2.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20240222-v1.22.2.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20240222-v1.22.2.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20240222-v1.22.2.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.22.2)

[v1.22.1 (2024-01-05) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20240105-v1.22.1.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20240105-v1.22.1.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20240105-v1.22.1.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20240105-v1.22.1.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20240105-v1.22.1.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.22.1)

[v1.22.0 (2023-12-27) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20231227-v1.22.0.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20231227-v1.22.0.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20231227-v1.22.0.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20231227-v1.22.0.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20231227-v1.22.0.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.22.0)

[v1.21.0 (2023-10-05) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20231005-v1.21.0.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20231005-v1.21.0.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20231005-v1.21.0.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20231005-v1.21.0.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20231005-v1.21.0.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.21.0)

[v1.20.0 (2023-04-26) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20230426-v1.20.0.uf2) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20230426-v1.20.0.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20230426-v1.20.0.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20230426-v1.20.0.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.20.0)

[v1.19.1 (2022-06-18) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20220618-v1.19.1.uf2) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20220618-v1.19.1.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20220618-v1.19.1.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20220618-v1.19.1.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.19.1)

[v1.18 (2022-01-17) .bin](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20220117-v1.18.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20220117-v1.18.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20220117-v1.18.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.18)

### Preview builds

[v1.27.0-preview.491.g3f796b687b (2025-12-03) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251203-v1.27.0-preview.491.g3f796b687b.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251203-v1.27.0-preview.491.g3f796b687b.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251203-v1.27.0-preview.491.g3f796b687b.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251203-v1.27.0-preview.491.g3f796b687b.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251203-v1.27.0-preview.491.g3f796b687b.map)

[v1.27.0-preview.490.g0b1a6bebae (2025-12-03) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251203-v1.27.0-preview.490.g0b1a6bebae.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251203-v1.27.0-preview.490.g0b1a6bebae.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251203-v1.27.0-preview.490.g0b1a6bebae.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251203-v1.27.0-preview.490.g0b1a6bebae.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251203-v1.27.0-preview.490.g0b1a6bebae.map)

[v1.27.0-preview.486.ge6a7dc1114 (2025-12-01) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251201-v1.27.0-preview.486.ge6a7dc1114.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251201-v1.27.0-preview.486.ge6a7dc1114.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251201-v1.27.0-preview.486.ge6a7dc1114.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251201-v1.27.0-preview.486.ge6a7dc1114.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251201-v1.27.0-preview.486.ge6a7dc1114.map)

[v1.27.0-preview.482.g8dc05cdba3 (2025-12-01) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251201-v1.27.0-preview.482.g8dc05cdba3.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251201-v1.27.0-preview.482.g8dc05cdba3.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251201-v1.27.0-preview.482.g8dc05cdba3.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251201-v1.27.0-preview.482.g8dc05cdba3.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251201-v1.27.0-preview.482.g8dc05cdba3.map)

(These are automatic builds of the development branch for the next release)

## Firmware (Support for Octal-SPIRAM)

### Releases

**[v1.26.1 (2025-09-11) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20250911-v1.26.1.uf2)** 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20250911-v1.26.1.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20250911-v1.26.1.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20250911-v1.26.1.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20250911-v1.26.1.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.26.1) 
(latest)

[v1.26.0 (2025-08-09) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20250809-v1.26.0.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20250809-v1.26.0.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20250809-v1.26.0.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20250809-v1.26.0.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20250809-v1.26.0.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.26.0)

[v1.25.0 (2025-04-15) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20250415-v1.25.0.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20250415-v1.25.0.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20250415-v1.25.0.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20250415-v1.25.0.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20250415-v1.25.0.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.25.0)

[v1.24.1 (2024-11-29) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20241129-v1.24.1.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20241129-v1.24.1.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20241129-v1.24.1.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20241129-v1.24.1.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20241129-v1.24.1.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.24.1)

[v1.24.0 (2024-10-25) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20241025-v1.24.0.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20241025-v1.24.0.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20241025-v1.24.0.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20241025-v1.24.0.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20241025-v1.24.0.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.24.0)

[v1.23.0 (2024-06-02) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20240602-v1.23.0.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20240602-v1.23.0.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20240602-v1.23.0.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20240602-v1.23.0.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20240602-v1.23.0.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.23.0)

[v1.22.2 (2024-02-22) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20240222-v1.22.2.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20240222-v1.22.2.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20240222-v1.22.2.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20240222-v1.22.2.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20240222-v1.22.2.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.22.2)

[v1.22.1 (2024-01-05) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20240105-v1.22.1.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20240105-v1.22.1.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20240105-v1.22.1.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20240105-v1.22.1.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20240105-v1.22.1.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.22.1)

[v1.22.0 (2023-12-27) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20231227-v1.22.0.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20231227-v1.22.0.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20231227-v1.22.0.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20231227-v1.22.0.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20231227-v1.22.0.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.22.0)

[v1.21.0 (2023-10-05) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20231005-v1.21.0.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20231005-v1.21.0.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20231005-v1.21.0.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20231005-v1.21.0.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20231005-v1.21.0.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.21.0)

[v1.20.0 (2023-04-26) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20230426-v1.20.0.uf2) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20230426-v1.20.0.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20230426-v1.20.0.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20230426-v1.20.0.map) 
/ [[Release notes]](https://github.com/micropython/micropython/releases/tag/v1.20.0)

### Preview builds

[v1.27.0-preview.491.g3f796b687b (2025-12-03) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251203-v1.27.0-preview.491.g3f796b687b.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251203-v1.27.0-preview.491.g3f796b687b.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251203-v1.27.0-preview.491.g3f796b687b.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251203-v1.27.0-preview.491.g3f796b687b.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251203-v1.27.0-preview.491.g3f796b687b.map)

[v1.27.0-preview.490.g0b1a6bebae (2025-12-03) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251203-v1.27.0-preview.490.g0b1a6bebae.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251203-v1.27.0-preview.490.g0b1a6bebae.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251203-v1.27.0-preview.490.g0b1a6bebae.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251203-v1.27.0-preview.490.g0b1a6bebae.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251203-v1.27.0-preview.490.g0b1a6bebae.map)

[v1.27.0-preview.486.ge6a7dc1114 (2025-12-01) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251201-v1.27.0-preview.486.ge6a7dc1114.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251201-v1.27.0-preview.486.ge6a7dc1114.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251201-v1.27.0-preview.486.ge6a7dc1114.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251201-v1.27.0-preview.486.ge6a7dc1114.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251201-v1.27.0-preview.486.ge6a7dc1114.map)

[v1.27.0-preview.482.g8dc05cdba3 (2025-12-01) .uf2](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251201-v1.27.0-preview.482.g8dc05cdba3.uf2) 
/ [[.app-bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251201-v1.27.0-preview.482.g8dc05cdba3.app-bin) 
/ [[.bin]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251201-v1.27.0-preview.482.g8dc05cdba3.bin) 
/ [[.elf]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251201-v1.27.0-preview.482.g8dc05cdba3.elf) 
/ [[.map]](https://micropython.org/resources/firmware/ESP32_GENERIC_S3-SPIRAM_OCT-20251201-v1.27.0-preview.482.g8dc05cdba3.map)

(These are automatic builds of the development branch for the next release)
