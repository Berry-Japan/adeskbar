Name:		adeskbar
Version:	0.4.2
Release:	b1
Summary:	A launcher for OpenBox
Group:		User Interface/Desktops
License:	GPLv3
URL:		http://www.ad-comp.be/?category/ADesk-Bar
Source0:	http://www.ad-comp.be/public/projets/ADeskBar/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:	python
Requires:	python >= 2.6
Requires:	pygtk2
Requires:	pygobject2
#Requires:	python-cairo
Requires:	gnome-menus, gnome-python2-libwnck, pyxdg
Requires:	python-alsaaudio, python-xlib

BuildArchitectures: noarch

%description
ADesk Bar is a easy, simple, unobtrusive application launcher for Openbox, yet
also works great under Gnome or XFCE.

%prep
%setup -q -n %{name}-%{version}

%build
# Uh... Nothing to build.
sed -e 's/x-www-browser/htmlview/' -i src/plugins/conf/searchbox.py

%install
# Taken from the included install.sh file.
pyc=$(find . -name '*.pyc')
for file in $pyc; do rm $file; done

install -d $RPM_BUILD_ROOT/usr/share/adeskbar
install -d $RPM_BUILD_ROOT/usr/bin
install -d $RPM_BUILD_ROOT/usr/share/applications
install -d $RPM_BUILD_ROOT/usr/share/pixmaps

# mkdir $RPM_BUILD_ROOT/usr/share/adeskbar
cp -a src/*  $RPM_BUILD_ROOT/usr/share/adeskbar
# chown -R root: $RPM_BUILD_ROOT/usr/share/adeskbar
cp src/images/adeskbar.png $RPM_BUILD_ROOT/usr/share/pixmaps/
cp adeskbar.desktop $RPM_BUILD_ROOT/usr/share/applications/
cp adeskbar.sh $RPM_BUILD_ROOT/usr/bin/adeskbar


desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-System-Configuration" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_datadir}/%{name}/*
%{_datadir}/applications/
%{_datadir}/pixmaps/
%{_bindir}/%{name}

%changelog
* Mon Dec 20 2010 Yuichiro Nakada <berry@rberry.co.cc> - 0.4.2
- Create for Berry Linux
