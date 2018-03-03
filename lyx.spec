Summary:	A word processor for the Desktop Environment
Name:		lyx
Version:	2.2.3
Release:	1
Group:		Office
License:	GPLv2+
Url:		http://www.lyx.org/
Source0:	ftp://ftp.lyx.org/pub/lyx/stable/%(echo %{version}|cut -d. -f1-2).x/%{name}-%{version}.tar.xz
# use xdg-open instead of hard coded applications to open files
# sent to upstream developers by fhimpe on 4 Jun 2009
Patch0:		lyx-2.1.4-xdg_open.patch
# weird but necessary to compare the supported qt version
# see http://comments.gmane.org/gmane.editors.lyx.devel/137498
BuildRequires:	bc
BuildRequires:	gettext
BuildRequires:	ghostscript
BuildRequires:	groff-base
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(python2)
BuildRequires:	sgml-tools
BuildRequires:	texinfo
BuildRequires:	texlive-collection-latex
BuildRequires:	boost-devel
BuildRequires:	gettext-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(hunspell)
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5Gui)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	pkgconfig(enchant)
BuildRequires:	pkgconfig(xpm)
Requires:	fonts-ttf-latex 
Requires:	xdg-utils
Requires:	texlive
Requires:	texlive-scheme-full

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
%apply_patches
autoreconf -fi -Iconfig

%build
export PATH=%{_qt5_bindir}:$PATH
export PYTHON=%{__python2}

%configure \
	--enable-qt5 \
	--with-qt-dir=%_qt5_bindir \
	--disable-rpath \
	--without-included-boost \
	--enable-optimization="%{optflags}" \
	--with-enchant \
	--with-hunspell \
	--disable-silent-rules
%make

%install
%makeinstall_std

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/lyx.desktop << EOF
[Desktop Entry]
Name=LyX
Comment=TeX document processor - especially good at scientific documents
Exec=%{_bindir}/lyx
Icon=lyx
Terminal=false
Type=Application
Categories=Qt;Office;WordProcessor;X-MandrivaLinux-CrossDesktop;
MimeType=application/x-lyx;
EOF

## icons
mkdir -p %{buildroot}/%{_liconsdir}
convert -size 48x48 development/Win32/packaging/icons/lyx_32x32.png %{buildroot}/%{_liconsdir}/%{name}.png
mkdir -p %{buildroot}/%{_iconsdir}
cp development/Win32/packaging/icons/lyx_32x32.png %{buildroot}/%{_iconsdir}/%{name}.png
mkdir -p %{buildroot}/%{_miconsdir}
convert -size 16x16 development/Win32/packaging/icons/lyx_32x32.png %{buildroot}/%{_miconsdir}/%{name}.png

## Set up the lyx-specific class files where TeX can see then
TEXMF=%{_datadir}/texmf
mkdir -p %{buildroot}${TEXMF}/tex/latex
cp -r %{buildroot}%{_datadir}/lyx/tex %{buildroot}${TEXMF}/tex/latex/lyx
chmod +x %{buildroot}%{_datadir}/lyx/configure.py
rm -f %{buildroot}%{_bindir}/listerrors

# (tpg) fix bug #1190
sed -i -e "s,/usr/bin/env python,%{__python2},g" %{buildroot}%{_datadir}/lyx/configure.py

%find_lang %{name}

find %{buildroot}%{_datadir}/%{name} -type f | sed -e "s@%{buildroot}@@g" \
	-e "s@%{_datadir}/%{name}/doc/\(..\)_@%lang(\1) %{_datadir}/%{name}/doc/\1_@g" \
	-e "s@\(%{_datadir}/%{name}/configure.py\)\$@%attr(755,root,root) \1@g" \
	-e "s@\(%{_datadir}/%{name}/scripts/\)@%attr(755,root,root) \1@g" \
	-e "s@\(%{_datadir}/%{name}/lyx2lyx/\)@%attr(755,root,root) \1@g" \
	>> %{name}.lang
find %{buildroot}%{_datadir}/%{name} -type d | sed -e "s@%{buildroot}@%dir @g" >> %{name}.lang

%post
## Fix the TeX file hash
texhash
## Before configuring lyx for the local system
## PATH needs to be imported
if [ -f /etc/profile ]; then
    . /etc/profile
fi
## Now configure LyX
cd %{_datadir}/lyx
./configure.py > /dev/null

%files -f %{name}.lang
%doc README ANNOUNCE
%{_bindir}/%{name}
%{_bindir}/lyxclient
%{_bindir}/tex2lyx
%{_datadir}/applications/lyx.desktop
%{_datadir}/texmf/tex/latex/lyx
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{name}.*
%{_miconsdir}/%{name}.png
%{_mandir}/man1/*

