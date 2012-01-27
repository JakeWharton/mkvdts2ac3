
.PHONY: dist clean dist-dir dist-rpm dist-dpkg

PACKAGE:=mkvdts2ac3
VERSION:=1.6.0
REVISION:=2

MKDIR?=mkdir
CP?=cp --archive

DIST_DPKG:=$(shell mktemp -d)

dist-dir:
	$(MKDIR) dist

dist: dist-dpkg dist-rpm

dist-rpm:
	@echo TBD

dist-dpkg: dist-dir
	$(MKDIR) -p $(DIST_DPKG)/DEBIAN
	$(MKDIR) -p $(DIST_DPKG)/usr/bin
	$(CP) mkvdts2ac3.sh $(DIST_DPKG)/usr/bin/mkvdts2ac3
	$(CP) $(PACKAGE)_dpkg.txt $(DIST_DPKG)/DEBIAN/control
	$(CP) CHANGELOG.md LICENSE.txt $(DIST_DPKG)/DEBIAN
	dpkg -b $(DIST_DPKG) dist/$(PACKAGE)_$(VERSION)-$(REVISION).all.deb
	$(RM) -r $(DIST_DPKG)

clean:
	$(RM) -r dist
