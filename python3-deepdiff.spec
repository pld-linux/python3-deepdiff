# Conditional build:
%bcond_with	doc	# API documentation
%bcond_with	tests	# unit tests

%define		module	deepdiff
Summary:	Deep Difference and search of any Python object/data
Name:		python3-%{module}
Version:	8.6.2
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/deepdiff/
Source0:	https://files.pythonhosted.org/packages/source/d/deepdiff/%{module}-%{version}.tar.gz
# Source0-md5:	14d6e7aa4f0c86c9b80f7f1a9c33cad1
URL:		https://github.com/seperman/deepdiff
BuildRequires:	python3-build
BuildRequires:	python3-flit_core >= 3.11
BuildRequires:	python3-flit_core < 4
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
%if %{with tests}
#BuildRequires:	python3-
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.9
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

# library module, not a script
%{__sed} -i -e "1{/^#!/d}" deepdiff/diff.py

%build
%py3_build_pyproject

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

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/deep
%dir %{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}/*.py
%{py3_sitescriptdir}/%{module}/__pycache__
%{py3_sitescriptdir}/%{module}/py.typed
%{py3_sitescriptdir}/%{module}-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
