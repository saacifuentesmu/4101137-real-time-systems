# Pre-course setup — before week 1

Work **at home, before the first class**. Week 1 only *verifies* this; if you show
up without the environment, you lose the lab.

## 1. Zephyr environment

Follow Zephyr's official guide ([Getting Started](https://docs.zephyrproject.org/latest/develop/getting_started/index.html))
on native Linux or WSL2. For WSL2 there's a tested guide from the instructor:
[wsl2-embedded-dev-setup](https://github.com/saacifuentesmu/wsl2-embedded-dev-setup).

By the end you must have: `west`, the Zephyr SDK, and a working workspace
(`west init` + `west update`).

## 2. Build the course's two targets

```bash
west build -p -b stm32c0116_dk  zephyr/samples/basic/blinky
west build -p -b native_sim     zephyr/samples/hello_world
./build/zephyr/zephyr.exe        # native_sim runs on your PC
```

Both builds must finish without errors. (The ESP32-S3 joins in week 3 — you don't
need it yet.)

## 3. Serial-port access (Linux/WSL2)

```bash
sudo usermod -aG dialout $USER   # log out and back in
```

On WSL2: install `usbipd-win` on Windows to pass USB through to Linux (covered in
the guide).

## Week-1 checklist

- [ ] `west --version` responds.
- [ ] blinky builds for `stm32c0116_dk`.
- [ ] `hello_world` runs on `native_sim`.
- [ ] Your user is in the `dialout` group (or equivalent).
- [ ] VS Code with the C/C++ extension (or your preferred editor) opens the workspace.

Problems? Bring the exact error (text, not a photo) to week 1 — the lab starts by
fixing whatever is missing.
