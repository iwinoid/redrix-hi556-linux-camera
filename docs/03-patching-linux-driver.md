# Patching the Linux HI556 Driver

## Changes

Two changes are applied to `hi556.c`:

1. **Windows H8B5 register values** for the 2592x1944 mode.
2. **Calibrated AWB gains** from the AIQB file to reduce the green cast.

The patched source is in:

```text
drivers/hi556-h8b5.c
```

A prebuilt module is in:

```text
drivers/prebuilt/hi556-h8b5.ko
```

## Build

```bash
cd drivers/hi556-h8b5-build
make -C /lib/modules/$(uname -r)/build M=$PWD modules
```

## Install for next boot

```bash
sudo cp drivers/prebuilt/hi556-h8b5.ko /lib/modules/$(uname -r)/updates/hi556.ko
sudo depmod -a
sudo reboot
```

## Verify

```bash
modinfo hi556 | grep filename
```

Should point to:

```text
/lib/modules/.../updates/hi556.ko
```

## AWB gains used

From `HI556_H8B5_ADL.aiqb`, the 5024K daylight gains were chosen:

```text
R gain ≈ 1.9966
B gain ≈ 1.4936
G gain = 1.0
```

These are applied in `hi556_update_digital_gain()` by writing different MWB gains for R/B vs G.
