
import pygame
import os, sys, ctypes

__df = None
__nf = None
__if = None

def debugfont():
    global __df
    if __df == None:
        __df = pygame.font.Font("freesansbold.ttf", 12)
    
    return __df

def infofont():
    global __if
    if __if == None:
        __if = pygame.font.Font("freesansbold.ttf", 16)
    
    return __if
    
def namefont():
    global __nf
    if __nf == None:
        __nf = pygame.font.Font("freesansbold.ttf", 22)
    
    return __nf

def wrapcircle(surface, color, pos, radius, worldsize, thickness=0):
    pygame.draw.circle(surface, color, pos, radius, thickness)
    if pos[0] < radius:
        pygame.draw.circle(surface, color, (pos[0] + worldsize[0], pos[1]), radius, thickness)
    elif pos[0] > worldsize[0] - radius:
        pygame.draw.circle(surface, color, (pos[0] - worldsize[0], pos[1]), radius, thickness)

    if pos[1] < radius:
        pygame.draw.circle(surface, color, (pos[0], pos[1] + worldsize[1]), radius, thickness)
    elif pos[1] > worldsize[1] - radius:
        pygame.draw.circle(surface, color, (pos[0], pos[1] - worldsize[1]), radius, thickness)

def detect_resolution(cfg):
    rez = None
    pygame.display.init()

    # Disable DPI Scaling in Windows for exact pixel matching!
    if os.name == "nt" and sys.getwindowsversion()[0] >= 6:
        user32 = ctypes.windll.user32

        if not cfg.getboolean("Application", "dpi_aware"):
            print("Disabling DPI Awareness")
            user32.SetProcessDPIAware()
        else:
            hwnd = pygame.display.get_wm_info()["window"]
            dpi = user32.GetDpiForWindow(hwnd)
            print("Current DPI: ", dpi)
            if rez == None:
                rez = (user32.GetSystemMetricsForDpi(0, dpi), user32.GetSystemMetricsForDpi(1, dpi))
                print("Scaled Resolution: ", rez)

    if rez == None:    
        rez = pygame.display.list_modes()[0]

    return rez