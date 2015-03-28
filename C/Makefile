all:
	gcc -fpic -c screenshot.c
	gcc -shared -o libscreenshot.so screenshot.o -lX11 -lXext
	gcc -o screenshot screenshot.o -lX11 -lXext

clean:
	rm -rf libscreenshot.so screenshot.o
