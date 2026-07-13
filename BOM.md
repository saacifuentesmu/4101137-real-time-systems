# Lista de Componentes (BOM) — por grupo de 2–3 estudiantes

Los laboratorios se hacen en grupos de 2–3. Cada grupo compra un **Kit Control**
(módulos 0–5 y proyecto final). El **Kit Hub** (módulos 6–7) es uno por grupo grande
(4–6, dos grupos fusionados) o lo presta el laboratorio.

> Precios de referencia julio 2026 en COP; **verificar en el enlace antes de
> comprar** (fluctúan por vendedor). En AliExpress el total baja ~40–60 % pero tarda
> 2–5 semanas y puede pasar por aduana: pedir a más tardar en la semana 1–2 del
> semestre (solo para lo que se usa de la semana 5 en adelante — la placa cómprenla
> local).

## Kit Control (uno por grupo de 2–3)

| # | Componente | Cant. | Para qué | MercadoLibre CO (aprox.) | AliExpress (aprox.) |
|---|-----------|-------|----------|--------------------------|---------------------|
| 1 | **ESP32-S3 DevKitC-1 N16R8** (o YD-ESP32-S3 N8R2) | 1 | La placa del curso | [$41.000–85.000](https://listado.mercadolibre.com.co/esp32-s3-devkitc) ([opción 1](https://articulo.mercadolibre.com.co/MCO-1494660367-tarjeta-desarrollo-esp32-s3-n16r8-doble-puerto-usb-tipo-c-_JM), [opción 2](https://articulo.mercadolibre.com.co/MCO-1998898288-yd-esp32-s3-devkitc-n8r2-wroom-wifi-bluetooth-usb-dual-_JM)) | US$6–10 |
| 2 | **Analizador lógico USB 8 ch 24 MHz** | 1 | Medir latencia/jitter — el instrumento central del curso | [$30.000–50.000](https://listado.mercadolibre.com.co/analizador-logico-usb) ([con ganchos](https://articulo.mercadolibre.com.co/MCO-1420558229-analizador-logico-usb-24mhz-8ch-12-ganchos-de-prueba-cab-_JM)); también [Electronilab](https://electronilab.co/tienda/analizador-logico-usb-8-canales-24mhz/) | US$4–6 |
| 3 | **Pantalla TFT táctil 2.8" ILI9341 (SPI)** | 1 | GUI local del nodo Control (LVGL sobre Zephyr) | [$35.000–60.000](https://listado.mercadolibre.com.co/ili9341) ([ejemplo](https://articulo.mercadolibre.com.co/MCO-2885980352-lcd-tft-tactil-28-pulgadas-240x320-ili9341-esp32-arduino-_JM)) | US$6–9 |
| 4 | **Sensor de flujo YF-S401** (o YF-S201) | 1 | "Caudal de riego": pulsos Hall → interrupciones, tarea dura de muestreo | [$15.000–30.000](https://listado.mercadolibre.com.co/sensor-de-flujo-yf-s201) ([YF-S401](https://articulo.mercadolibre.com.co/MCO-865008893-sensor-de-flujo-de-agua-yf-s401-_JM)) | US$3–5 |
| 5 | **Mini bomba sumergible 5 V** + manguera | 1 | El actuador del lazo de control | [$8.000–15.000](https://listado.mercadolibre.com.co/mini-bombas-de-agua-arduino) ([ejemplo](https://articulo.mercadolibre.com.co/MCO-524609873-mini-bomba-de-agua-sumergible-5v-proyectos-arduino-_JM)) | US$2–3 |
| 6 | **Driver puente H MX1508/L298N** (o módulo MOSFET) | 1 | PWM hacia la bomba (nunca directo al GPIO) | $8.000–15.000 ([buscar](https://listado.mercadolibre.com.co/modulo-driver-motor-mx1508)) | US$1–2 |
| 7 | **Servo SG90** | 1 | "Válvula": segunda salida con deadline | $10.000–15.000 ([buscar](https://listado.mercadolibre.com.co/servo-sg90)) | US$2 |
| 8 | **DS18B20** (sonda) o termistor | 1 | Temperatura: sensor lento para la telemetría suave | $8.000–15.000 ([buscar](https://listado.mercadolibre.com.co/sensor-ds18b20)) | US$1–2 |
| 9 | **Kit protoboard**: protoboard 830, jumpers M-M/M-H, LEDs, resistencias, botones, potenciómetro ("presión"), fuente de protoboard | 1 | Base de todos los laboratorios | $30.000–50.000 ([buscar kit](https://listado.mercadolibre.com.co/kit-protoboard-arduino)) | US$6–10 |
| 10 | Cable USB-C **de datos** | 1–2 | Programación/monitor (verificar que no sea solo carga) | $8.000–15.000 | US$1–2 |

**Total Kit Control**: ~**$190.000–320.000 COP** por grupo (≈ $65.000–110.000 por
estudiante en grupos de 3). Vía AliExpress: ≈ **US$32–50** + envío.

## Kit Hub (uno por grupo grande de 4–6, módulos 6–7)

| # | Componente | Cant. | Para qué | Precio aprox. |
|---|-----------|-------|----------|---------------|
| 11 | **Raspberry Pi 4 (4 GB)** o Pi 5 + microSD 32 GB + fuente oficial | 1 | El Hub: PREEMPT_RT, `SCHED_DEADLINE`, GUI, enrutamiento | [$350.000–550.000](https://listado.mercadolibre.com.co/raspberry-pi-4) (verificar; también [Sigma](https://www.sigmaelectronica.net/fabricante/raspberry-pi/)) |
| 12 | Pantalla del Hub | 1 | GUI local | Opción A: **HMI web** (navegador del portátil) — $0. Opción B: monitor HDMI del laboratorio — $0. Opción C: táctil 7" ($200.000–300.000), solo si el grupo la quiere |

> **Recomendación**: para contener el costo, la GUI del Hub se diseña como HMI web o
> LVGL sobre HDMI del laboratorio; la pantalla táctil 7" es opcional. Si el
> departamento puede prestar 4–6 Raspberry Pi, el Kit Hub baja a solo la microSD.

## Tiendas locales alternativas (Colombia)

[Electronilab](https://electronilab.co) · [Sigma Electrónica](https://www.sigmaelectronica.net) ·
Vistronica · La Red Electrónica — a veces mejor precio/stock que MercadoLibre para
sensores y módulos; envío nacional a Manizales.

## Cuándo se necesita cada cosa

- **Semana 1**: placa (#1) y cable (#10) — comprar local, sin esperar AliExpress.
- **Semana 3–4**: analizador lógico (#2), kit protoboard (#9), potenciómetro.
- **Semana 5+**: bomba, driver, flujo, servo, DS18B20, pantalla TFT (#3–8).
- **Semana 11**: Kit Hub (#11–12).
