# Setup previo — antes de la semana 1

Trabajo **en casa, antes de la primera clase**. La semana 1 solo *verifica* esto;
si llegas sin el entorno, pierdes el lab.

## 1. Entorno Zephyr

Sigue la guía oficial de Zephyr ([Getting Started](https://docs.zephyrproject.org/latest/develop/getting_started/index.html))
en Linux nativo o WSL2. Para WSL2 hay una guía probada del profesor:
[wsl2-embedded-dev-setup](https://github.com/saacifuentesmu/wsl2-embedded-dev-setup).

Al final debes tener: `west`, el SDK de Zephyr, y el workspace (`west init` +
`west update`) funcionando.

## 2. Compila los dos targets del curso

```bash
west build -p -b stm32c0116_dk  zephyr/samples/basic/blinky
west build -p -b native_sim     zephyr/samples/hello_world
./build/zephyr/zephyr.exe        # native_sim corre en tu PC
```

Ambas compilaciones deben terminar sin errores. (La ESP32-S3 se agrega en la
semana 3 — no la necesitas aún.)

## 3. Acceso al puerto serial (Linux/WSL2)

```bash
sudo usermod -aG dialout $USER   # cerrar sesión y volver a entrar
```

En WSL2: instala `usbipd-win` en Windows para pasar el USB a Linux (está en la guía).

## Checklist para la semana 1

- [ ] `west --version` responde.
- [ ] blinky compila para `stm32c0116_dk`.
- [ ] `hello_world` corre en `native_sim`.
- [ ] Tu usuario está en el grupo `dialout` (o equivalente).
- [ ] VS Code con la extensión C/C++ (o tu editor preferido) abre el workspace.

¿Problemas? Trae el error exacto (texto, no foto) a la semana 1 — el lab empieza
resolviendo lo que falte.
