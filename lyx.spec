Name:		lyx
Summary:	A word processor for the Desktop Environment
Version:	1.4.4
Release:	%mkrel 1

Source:		ftp://ftp.lyx.org/pub/lyx/stable/%name-%version.tar.bz2
URL:		http://www.lyx.org/
Group:		Office

BuildRequires:	qt3-devel xpm-devel libjpeg-devel
BuildRequires:	gtkmm2.4-devel libglademm2.4-devel
#BuildRequires:	chrpath
BuildRequires:	gcc-c++
BuildRequires:	gettext
BuildRequires:	ghostscript groff-for-man sgml-tools
BuildRequires:	tetex-dvips tetex-latex texinfo
BuildRequires:	libboost-devel
BuildRequires:	aspell-devel
BuildRequires:	python
BuildRequires:	ImageMagick

Requires:	tetex tetex-latex tetex-dvips fonts-ttf-latex

BuildRoot:	%_tmppath/%name-%version-%release-root
License:	GPL

%description
LyX is a modern approach of writing documents with a computer
which breaks with the tradition of the obsolete typewriter
concept.  It is designed for people who want a professional
output with a minimum of time effort, without becoming specia-
lists in typesetting.  Compared to common word processors LyX
will increase the productivity a lot, since most of the type-
setting will be done by the computer, not the author.  With LyX
the author can concentrate on the contents of his writing,
since the computer will take care of the look.

%package	gtk
Summary:	LyX document processor - GTK frontend
Group:		Office
Requires:	%name

%description	gtk
GTK2 frontend for LyX.

This is currently experimental, and not all features are implemented, but it
should be stable and full featured enough to use from time to time.

%prep
%setup -q

%build
%define common_opt --without-aiksaurus --enable-compression-support
mkdir qt-build
pushd qt-build
CONFIGURE_TOP=.. %configure2_5x --with-frontend=qt --with-qt-dir=/usr/lib/qt3 --with-qt-libraries=%{_prefix}/lib/qt3/%{_lib} --disable-rpath %common_opt
%make
popd
mkdir gtk-build
pushd gtk-build
CONFIGURE_TOP=.. %configure2_5x --with-frontend=gtk %common_opt
%make
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd qt-build
%makeinstall_std
mv %buildroot/%_bindir/%name %buildroot/%name
popd
pushd gtk-build
%makeinstall_std
mv %buildroot/%_bindir/lyx %buildroot/%_bindir/lyx-gtk
popd
mv %buildroot/%name %buildroot/%_bindir/%name

#mdk menu
mkdir -p $RPM_BUILD_ROOT/%{_menudir}
cat >$RPM_BUILD_ROOT%{_menudir}/lyx <<EOF
?package(lyx): command="%{_bindir}/lyx" \
needs="X11" \
icon="%name.png" \
section="Office/Wordprocessors" \
mimetypes="text/x-lyx" \
title="LyX" \
longtitle="TeX document processor - especially good at scientific documents" \
xdg="true"
EOF

cat >$RPM_BUILD_ROOT%{_menudir}/lyx-gtk <<EOF
?package(lyx-gtk): command="%{_bindir}/lyx-gtk" \
needs="X11" \
icon="%name.png" \
section="Office/Wordprocessors" \
mimetypes="text/x-lyx" \
title="LyX" \
longtitle="TeX document processor - Experimental GTK Frontend" \
xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-lyx.desktop << EOF
[Desktop Entry]
Name=LyX
Comment=TeX document processor - especially good at scientific documents
Exec=%{_bindir}/lyx
Icon=lyx
Terminal=false
Type=Application
Categories=Qt;KDE;Office;X-MandrivaLinux-Office-Wordprocessors
EOF

cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-lyx-gtk.desktop << EOF
[Desktop Entry]
Name=LyX (GTK)
Comment=TeX document processor - Experimental GTK Frontend
Exec=%{_bindir}/lyx-gtk
Icon=lyx
Terminal=false
Type=Application
Categories=GTK;Office;X-MandrivaLinux-Office-Wordprocessors
EOF


## icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
convert -size 48x48 development/Win32/packaging/icons/lyx_32x32.png $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
cp development/Win32/packaging/icons/lyx_32x32.png $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
convert -size 16x16 development/Win32/packaging/icons/lyx_32x32.png $RPM_BUILD_ROOT/%_miconsdir/%name.png

## Set up the lyx-specific class files where TeX can see then
TEXMF=%{_datadir}/texmf
mkdir -p $RPM_BUILD_ROOT${TEXMF}/tex/latex
cp -r $RPM_BUILD_ROOT%_datadir/lyx/tex $RPM_BUILD_ROOT${TEXMF}/tex/latex/lyx
chmod +x $RPM_BUILD_ROOT%_datadir/lyx/configure.py
rm -f $RPM_BUILD_ROOT%_bindir/listerrors

%find_lang %name
find $RPM_BUILD_ROOT%_datadir/%name -type f | sed -e "s@$RPM_BUILD_ROOT@@g" \
	-e "s@%_datadir/%name/doc/\(..\)_@%lang(\1) %_datadir/%name/doc/\1_@g" \
	-e "s@\(%_datadir/%name/configure.py\)\$@%attr(755,root,root) \1@g" \
	-e "s@\(%_datadir/%name/scripts/\)@%attr(755,root,root) \1@g" \
	-e "s@\(%_datadir/%name/lyx2lyx/\)@%attr(755,root,root) \1@g" \
	>> %name.lang
find $RPM_BUILD_ROOT%_datadir/%name -type d | sed -e "s@$RPM_BUILD_ROOT@%dir @g" >> %name.lang

#chrpath -d $RPM_BUILD_ROOT%_bindir/%name

%post
%update_menus
## Fix the TeX file hash
texhash
## Before configuring lyx for the local system 
## PATH needs to be imported
if [ -f /etc/profile ]; then
    . /etc/profile
fi
## Now configure LyX
cd %_datadir/lyx
./configure.py > /dev/null

%postun
%clean_menus

%post gtk
%update_menus

%postun gtk
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr (-,root,root)
%doc INSTALL README ANNOUNCE NEWS INSTALL.autoconf
%doc UPGRADING COPYING 
%_bindir/%name
%_bindir/lyxclient
%_bindir/tex2lyx
%_mandir/man1/*
#%_datadir/%name
%_datadir/texmf/tex/latex/lyx
%_menudir/%name
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png
%_datadir/applications/mandriva-lyx.desktop

%files gtk
%defattr (-,root,root)
%_bindir/lyx-gtk
#%_datadir/glade/*
%_menudir/lyx-gtk
%_datadir/applications/mandriva-lyx-gtk.desktop



