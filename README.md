PsiReporter
A framework for running regular reports

This is a simple framework that solves the problem of wanting to output results of different pieces of code at different periodic intervals.

There are two different types of plugins:

Reporters

Reporters create reports. Those reports can be anything you'd like.

Senders

Senders send reports somewhere. Store them in a database, print them to stdout, do fancy message queue stuff. Who knows.

Why?

Because I needed something like this for a project. Small and simple. No need to get into advanced task schedulers or anything complicated like that.