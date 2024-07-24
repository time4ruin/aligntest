all: align

align: align_test.c
	gcc align_test.c -o test.out

clean:
	rm -f test.out
