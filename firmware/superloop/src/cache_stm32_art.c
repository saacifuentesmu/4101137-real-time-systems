/*
 * Zephyr enables the STM32L4/G4 ART accelerator in soc_early_init_hook().
 * This disables its instruction and data caches before the application starts.
 * Flash prefetch is disabled separately by CONFIG_STM32_FLASH_PREFETCH=n.
 */

#include <zephyr/init.h>

#if defined(CONFIG_SOC_SERIES_STM32L4X)
#include <stm32l4xx_ll_system.h>
#elif defined(CONFIG_SOC_SERIES_STM32G4X)
#include <stm32g4xx_ll_system.h>
#else
#error "Unsupported STM32 series for LAB_FLASH_CACHE_OFF"
#endif

static int lab_flash_cache_off(void)
{
	LL_FLASH_DisableInstCache();
	LL_FLASH_DisableDataCache();
	return 0;
}

SYS_INIT(lab_flash_cache_off, PRE_KERNEL_1, 0);
