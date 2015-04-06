#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <X11/extensions/XShm.h>
#include <stdio.h>
#include <stdlib.h>

/**
   Initialize a DisplayContext.
 **/ 
Display* open_display_context() {
  Display* disp = XOpenDisplay(NULL);
  // fprintf(stderr, "Display: %p\n", (void *) disp);
  return disp;
}

/**
   Close a DisplayContext.
 **/ 
void close_display_context(Display* disp) {
  XCloseDisplay(disp);
}


/**
   Take a screenshot of the given rectangle using the given
   DisplayContext.
 **/
XImage* screenshot(Display* disp, int x, int y, 
                   int width, int height) {
  // fprintf(stderr, "Display: %p\n", (void *) disp);
  // fprintf(stderr, "Coord: %d, %d, %d, %d\n", x, y, width, height);
  Window root = DefaultRootWindow(disp);
  return XGetImage(disp, (Drawable) root, x, y, width, height, AllPlanes, ZPixmap);
}

/**
   Destroy an XImage
 **/
void destroy_image(XImage* img) {
  XDestroyImage(img);
}

int main (int argc, char *argv[]) {
  // Test the API
  Display* disp = open_display_context();
  XImage* img = screenshot(disp, 700, 500, 400, 300);
  printf("Test :%lu", XGetPixel(img, 200, 0));
  destroy_image(img);
  close_display_context(disp);
}
