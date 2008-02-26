Name:		lyx
Summary:	A word processor for the Desktop Environment
Version:	1.5.4
Release:	%mkrel 1

Source:		ftp://ftp.lyx.org/pub/lyx/stable/%name-%version.tar.bz2
URL:		http://www.lyx.org/
Group:		Office

BuildRequires:	qt4-devel xpm-devel libjpeg-devel
#BuildRequires:	chrpath
BuildRequires:	gcc-c++
BuildRequires:	gettext
BuildRequires:	ghostscript groff-for-man sgml-tools
BuildRequires:	tetex-dvips tetex-latex texinfo
BuildRequires:	libboost-devel
BuildRequires:	aspell-devel
BuildRequires:	python
BuildRequires:	ImageMagick
Obsoletes:      lyx-gtk

Requires:	tetex tetex-latex tetex-dvips fonts-ttf-latex

BuildRoot:	%_tmppath/%name-%version-%release-root
License:	GPLv2

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

%prep
%setup -q

%build

%define common_opt --without-aiksaurus --enable-compression-support
mkdir qt-build
pushd qt-build
CONFIGURE_TOP=.. %configure --with-frontend=qt4 --with-qt-dir=/usr/lib/qt4 --with-qt-libraries=%{_prefix}/lib/qt4/%{_lib} --disable-rpath %common_opt
make
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd qt-build
%makeinstall_std
mv %buildroot/%_bindir/%name %buildroot/%name
popd
mv %buildroot/%name %buildroot/%_bindir/%name

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-lyx.desktop << EOF
[Desktop Entry]
Name=LyX
Comment=TeX document processor - especially good at scientific documents
Exec=%{_bindir}/lyx
Icon=lyx
Terminal=false
Type=Application
Categories=Qt;Office;WordProcessor;X-MandrivaLinux-CrossDesktop;
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

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr (-,root,root)
%doc README ANNOUNCE
%_bindir/%name
%_bindir/lyxclient
%_bindir/tex2lyx
%_mandir/man1/*
#%_datadir/%name
%_datadir/texmf/tex/latex/lyx
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png
%_datadir/applications/mandriva-lyx.desktop

