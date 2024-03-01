%global debug_package %{nil}

# Run tests in check section
%bcond_without check

# https://github.com/russross/blackfriday
%global import_path	github.com/russross/blackfriday/v2
%global goipath		github.com/russross/blackfriday
%global forgeurl	https://github.com/russross/blackfriday
Version:			2.1.0

%gometa

Summary:	A markdown processor for Go 
Name:		golang-github-russross-blackfriday

Release:	1
Source0:	https://github.com/russross/blackfriday/archive/v%{version}/blackfriday-%{version}.tar.gz
URL:		https://github.com/russross/blackfriday
License:	GPL
Group:		Development/Other
BuildRequires:	compiler(go-compiler)

%description
Blackfriday is a Markdown processor implemented in Go.  It
is paranoid about its input (so you can safely feed it
user-supplied data), it is fast, it supports common extensions
(tables, smart punctuation substitutions, etc.), and it is
safe for all utf-8 (unicode) input.

HTML output is currently supported, along with Smartypants
extensions.

It started as a translation from C of Sundown.

#-----------------------------------------------------------------------

%package devel
Summary:	%{summary}
Group:		Development/Other
BuildArch:	noarch

%description devel
%{description}

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.

%files devel -f devel.file-list
%license LICENSE.txt
%doc README.md

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n blackfriday-%{version}

%build
%gobuildroot -i %{import_path}
for cmd in $(ls -1 cmd) ; do
	%gobuild -o _bin/$cmd %{goipath}/cmd/$cmd
done

%install
%goinstall -i %{import_path} -o devel.file-list
for cmd in $(ls -1 _bin) ; do
  install -Dpm 0755 _bin/$cmd %{buildroot}%{_bindir}/$cmd
done

%check
%if %{with check}
%gochecks -i %{import_path}
%endif

