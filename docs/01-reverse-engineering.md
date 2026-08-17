# Reverse Engineering the Windows HI556 Driver

## Goal

Extract the sensor initialization register values that the Windows driver uses for the HI556 camera module on Redrix (H8B5).

## Tools used

- `radare2` + `r2ghidra` for PE analysis and decompilation
- `objdump`, `strings`, `python3` for binary inspection
- `7z` to unpack the OEM driver installer

## Steps

### 1. Obtain the Windows driver

HP ships an Intel IPU6 camera driver package. The file used here was:

```text
sp149028_Intel_IPU6_Camera_Driver.exe
```

It is a self-extracting archive. Unpack with:

```bash
7z x sp149028_Intel_IPU6_Camera_Driver.exe -o extracted/
```

Inside, the HI556 sensor driver is at:

```text
extracted/src/driver/hi556.sys
extracted/src/driver/graph_settings_HI556_H8B5_ADL.xml
extracted/src/driver/HI556_H8B5_ADL.aiqb
```

### 2. Load the driver in radare2

```bash
r2 -e bin.relocs.apply=true -A hi556.sys
```

Useful commands:

```text
iI          binary info
ii          imports
iE          exports
izz         all strings
axt @@ str.*   string xrefs
pdg @ addr  Ghidra decompiler pseudocode
```

No PDB was available. The binary records a PDB path but the file is not shipped.

### 3. Find the initialization register table

The Windows driver stores I2C register writes as a table in `.rdata`.

The table format observed is 16 bytes per entry:

```text
uint32 flag        (usually 0x00000002)
uint16 register
uint16 reserved
uint16 value
uint16 reserved
uint32 reserved
```

For the H8B5 module, the main mode table starts at file offset `0x20640`.

A Python script was used to parse and print the table; the result is in:

```text
calibration/windows_h8b5_mode_regs.txt
```

### 4. Key differences vs the mainline Linux driver

| Register | Linux original | Windows H8B5 |
|---|---|---|
| 0x004e | 0x0100 | 0x0700 |
| 0x0026 | 0x0030 | 0x0120 |
| 0x002c | 0x07c9 | 0x06cf |
| 0x0006 | 0x0814 | 0x0812 |
| 0x0a14 | 0x0798 | 0x05a4 |
| 0x0074 | 0x0812 | 0x0810 |
| 0x0070 | 0x0409 | 0x0408 |

These differences were the cause of the striped/garbage output in Linux.
