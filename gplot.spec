Summary:	GPLOT - CGM files processor
Summary(pl):	GPLOT - narzêdzie do przetwarzania plików CGM
Name:		gplot
Version:	4.3b2
Release:	2
Group:		X11/Applications/Graphics
License:	distributable if unchanged and without charge
Source0:	ftp://ftp.psc.edu/pub/gplot/%{name}.tar.Z
# Source0-md5:	b29be9573996be595eff2d7d1dd71849
Patch0:		%{name}-glibc.patch
Patch1:		%{name}-x.patch
Patch2:		%{name}-rletocgm.patch
Patch3:		%{name}-link.patch
BuildRequires:	XFree86-devel
BuildRequires:	motif-devel
BuildRequires:	netpbm-devel >= 10.0
BuildRequires:	urt-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GPLOT is a CGM (Computer Graphics Metafile) processor. CGM files come
in 3 flavours, Binary (dominant form), Clear Text (human readable),
and Character (more compact than Clear Text, but only 7 bits used per
byte) encodings. GPLOT will interpret and create Binary and Clear Text
files, I have not yet had requests for character encoding.

%description -l pl
GPLOT jest narzêdziem do przetwarzania plików CGM (Computer Graphics
Metafile). Pliki CGM wystêpuj± w trzech rodzajach: binarnym
(najczê¶ciej), czystym tekscie (czytelnym) i znakowym (7 bitów/bajt).
GPLOT interpretuje pliki binarne i czysty tekst.

%prep
%setup -q -c
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__make} gplot gplotaw gplotm drawcgm \
	CTR_FLAGS="-Dinctty" \
	DRV_FLAGS="-Dincxws -Dincps -Dinccgmc -Dinccgmb -Dincxl" \
	DRV_OBJ='ps.o cgmc.o cgmb.o xl.o $(XWS_OBJ)' \
	CTR_OBJ="tty.o" \
	XLIBS="-L/usr/X11R6/%{_lib} -lXmu -lXt -lX11" \
	MLIBS="-lXm -lXt -lX11" \
	CFLAGS="%{rpmcflags} -I/usr/X11R6/include"

rm -f devices.o

%{__make} gtex \
	CTR_FLAGS="-Dinctty" \
	DRV_FLAGS="-Dincps -Dinccgmc -Dinccgmb" \
	CTR_OBJ="tty.o" \
	CFLAGS="%{rpmcflags} -I/usr/X11R6/include"

cd drawcgm/rletocgm
%{__cc} %{rpmcflags} %{rpmldflags} -o pnmtocgm pnmtocgm.c -DUSE_UNIX -I.. \
	../drawcgm.a -L/usr/X11R6/%{_lib} -lX11 -lXt -lXmu -lm -lnetpbm
%{__cc} %{rpmcflags} %{rpmldflags} -o rletocgm rletocgm.c -DUSE_UNIX -I.. \
	../drawcgm.a -L/usr/X11R6/%{_lib} -lX11 -lXt -lXmu -lm -lrle

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}

install gplot gplotaw gplotm drawcgm/rletocgm/*tocgm $RPM_BUILD_ROOT%{_bindir}
install drawcgm/rletocgm/*tocgm.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.* gplot.txt gplot_install.doc gtex.doc drawcgm/drawcgm.doc
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
