# param_fitter autoconf file.
# Cengiz Gunay 2012-07-06

SHELL = /bin/sh

.SUFFIXES:
.SUFFIXES: .c

TARNAME = param_fitter
VERSION = 1.0b

DIRNAME = $(TARNAME)-$(VERSION)

all: 

dist: 
	mkdir $(DIRNAME)
	cp -a \@* $(DIRNAME)
	cp -a unittest $(DIRNAME)
	cp -a *.m $(DIRNAME)
	cp README.dist $(DIRNAME)/README
	cp COPYING $(DIRNAME)
	tar -cz --exclude-vcs --exclude=*~ -f $(DIRNAME).tar.gz $(DIRNAME)
	rm -rf $(DIRNAME)

distclean:
	rm -f *~
	rm -rf $(DIRNAME)

clean: 
	rm -f *~

