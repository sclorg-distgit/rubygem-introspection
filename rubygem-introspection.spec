%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from introspection-0.0.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name introspection

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.0.3
Release: 6%{?dist}
Summary: Dynamic inspection of the hierarchy of method definitions on a Ruby object
Group: Development/Languages
# https://github.com/floehopper/introspection/issues/1
License: MIT
URL: http://jamesmead.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Remove instantiator dependency.
# https://github.com/floehopper/introspection/issues/2
Patch0: %{pkg_name}-%{version}-update-dep.patch
# Fix MiniTest 5.x compatibility.
# https://github.com/floehopper/introspection/commit/b11609ece486c5558e06b4c18d916a21ad0c518a
Patch1: rubygem-introspection-0.0.3-Move-to-Minitest-5.patch

Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix_ruby}ruby
Requires: %{?scl_prefix}rubygem(metaclass) => 0.0.1
Requires: %{?scl_prefix}rubygem(metaclass) < 0.1
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix}rubygem(metaclass) => 0.0.1
BuildRequires: %{?scl_prefix}rubygem(metaclass) < 0.1
# Required to satisfy the 'blankslate' require. May be replaced
# by rubygem(blankslate) when available in Fedora.
BuildRequires: %{?scl_prefix}rubygem(builder)
# There is no #assert_nothing_raised in minitest 5.x
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Dynamic inspection of the hierarchy of method definitions on a Ruby object.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

pushd .%{gem_dir}
%patch0 -p0
popd

pushd .%{gem_instdir}
%patch1 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
# Disable Bundler.
sed -i '/bundler\/setup/ d' test/test_helper.rb

%{?scl:scl enable %{scl} - << \EOF}
ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
%{?scl:EOF}
popd

%files
%license %{gem_instdir}/COPYING.txt
%dir %{gem_instdir}
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%exclude %{gem_instdir}/introspection.gemspec
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/README.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/samples
%{gem_instdir}/test
%doc %{gem_docdir}

%changelog
* Sat Feb 20 2016 Pavel Valena <pvalena@redhat.com> - 0.0.3-6
- Add scl macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 19 2014 Vít Ondruch <vondruch@redhat.com> - 0.0.3-3
- Fix FTBFS in Rawhide (rhbz#1107144).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 07 2014 Vít Ondruch <vondruch@redhat.com> - 0.0.3-1
- Update to introspection 0.0.3.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Vít Ondruch <vondruch@redhat.com> - 0.0.2-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 0.0.2-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 04 2011 Vít Ondruch <vondruch@redhat.com> - 0.0.2-3
- Fix BuildRequires and test suite.
- Move README.md into -doc subpackage and mark it properly.

* Tue Oct 04 2011 Vít Ondruch <vondruch@redhat.com> - 0.0.2-2
- Clarified license.

* Mon Oct 03 2011 Vít Ondruch <vondruch@redhat.com> - 0.0.2-1
- Initial package
