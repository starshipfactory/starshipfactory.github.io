---
title: "{{ replace .Name "-" " " | title }}"
description: ""
date: {{ .Date }}
# Must match a key in data/authors.yaml, or the byline shows the date only.
author: ""
# Links this post to its translation in the other language. Must match on both.
translationKey: "{{ .Name }}"
draft: true
tags: []
categories: []
---
