Name:		lyx
Summary:	A word processor for the Desktop Environment
Version:	1.6.3
Release:	%mkrel 1
Source:		ftp://ftp.lyx.org/pub/lyx/stable/1.6.x/%name-%version.tar.bz2
# use xdg-open instead of hard coded applications to open files
# sent to upstream developers by fhimpe on 4 Jun 2009
Patch0:		lyx-1.6.3-xdg_open.patch
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
BuildRequires:	imagemagick
Obsoletes:      lyx-gtk

Requires:	tetex tetex-latex tetex-dvips fonts-ttf-latex
Requires:	xdg-utils

BuildRoot:	%_tmppath/%name-%version-%release-root
License:	GPLv2+

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
%patch0 -p1 -b .xdg-open

%build

%define common_opt --without-aiksaurus --enable-compression-support --without-included-boost
mkdir qt-build
pushd qt-build
CONFIGURE_TOP=.. %configure2_5x --with-frontend=qt4 --with-qt-dir=%{qt4dir} --with-qt-libraries=%{qt4lib} --disable-rpath %common_opt
make
popd

%install
rm -rf %{buildroot}
pushd qt-build
%makeinstall_std
mv %buildroot/%_bindir/%name %buildroot/%name
popd
mv %buildroot/%name %buildroot/%_bindir/%name

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-lyx.desktop << EOF
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
mkdir -p %{buildroot}/%_liconsdir
convert -size 48x48 development/Win32/packaging/icons/lyx_32x32.png %{buildroot}/%_liconsdir/%name.png
mkdir -p %{buildroot}/%_iconsdir
cp development/Win32/packaging/icons/lyx_32x32.png %{buildroot}/%_iconsdir/%name.png
mkdir -p %{buildroot}/%_miconsdir
convert -size 16x16 development/Win32/packaging/icons/lyx_32x32.png %{buildroot}/%_miconsdir/%name.png

## Set up the lyx-specific class files where TeX can see then
TEXMF=%{_datadir}/texmf
mkdir -p %{buildroot}${TEXMF}/tex/latex
cp -r %{buildroot}%_datadir/lyx/tex %{buildroot}${TEXMF}/tex/latex/lyx
chmod +x %{buildroot}%_datadir/lyx/configure.py
rm -f %{buildroot}%_bindir/listerrors

%find_lang %name
find %{buildroot}%_datadir/%name -type f | sed -e "s@%{buildroot}@@g" \
	-e "s@%_datadir/%name/doc/\(..\)_@%lang(\1) %_datadir/%name/doc/\1_@g" \
	-e "s@\(%_datadir/%name/configure.py\)\$@%attr(755,root,root) \1@g" \
	-e "s@\(%_datadir/%name/scripts/\)@%attr(755,root,root) \1@g" \
	-e "s@\(%_datadir/%name/lyx2lyx/\)@%attr(755,root,root) \1@g" \
	>> %name.lang
find %{buildroot}%_datadir/%name -type d | sed -e "s@%{buildroot}@%dir @g" >> %name.lang

#chrpath -d %{buildroot}%_bindir/%name

%post
%if %mdkversion < 200900
%update_menus
%endif
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

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

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
