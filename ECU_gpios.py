# ecu gpios
import gpiozero


# PFC status -----------------------------------------------------------------------------------------------------------
pfc_button = gpiozero.Button(2, pull_up=False, hold_time=1)


# Mode Button ----------------------------------------------------------------------------------------------------------
mode_button = gpiozero.Button(18, pull_up=True)


# Fuel and igniter digital outputs -------------------------------------------------------------------------------------
fps = gpiozero.DigitalOutputDevice(23)
fps.off()
ign = gpiozero.DigitalOutputDevice(24)
ign.off()


# end of script
