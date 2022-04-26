# Conditional build:
%bcond_without	doc	# API documentation
%bcond_with	tests	# unit tests

%define		module	deepdiff
Summary:	Deep Difference and search of any Python object/data
Name:		python3-%{module}
Version:	5.6.0
Release:	2
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.debian.net/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	a4ccc7101e5fce52b06bd3c1e89d113b
URL:		https://github.com/seperman/deepdiff
BuildRequires:	python3-modules >= 1:3.2
#BuildRequires:	python3-setuptools
%if %{with tests}
#BuildRequires:	python3-
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
- DeepDiff: Deep Difference of dictionaries, iterables, strings and
  other objects. It will recursively look for all the changes.
- DeepSearch: Search for objects within other objects.
- DeepHash: Hash any object based on their content.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest tests
%endif

%if %{with doc}
rm -rf docs/_build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/deep
%dir %{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}/*.py
%{py3_sitescriptdir}/%{module}/__pycache__
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
