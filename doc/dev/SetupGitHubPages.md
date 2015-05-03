---
title: Setup GitHub Pages
nav:
 - { page: "index.html", title: "Development" }
---

Installing [Jekyll](http://jekyllrb.com/) Builder
-------------------------

1. Install [Ruby 2.1.X](http://rubyinstaller.org/downloads/)
2. Install DevKet for Ruby 2.1.X under C:\Ruby21\DevKit (assuming C:\Ruby21 was Ruby Install Directory)
3. Open Command Prompt in C:\Ruby21\DevKit directory
4. ruby dk.rb init (ensure says found installed in C:\Ruby21)
5. ruby dk.rb review (ensure says C:\Ruby21 as directory)
6. ruby dk.rb install
7. gem install bundler
8. create **Gemfile** in repository root, with contents
	<pre><code>source 'https://rubygems.org'
gem 'github-pages'</code></pre>
9. type 'bundle install' in repository root