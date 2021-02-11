Title: Virtual K-12 Tableau User Group - 14 January 2021
Date: 2021-01-14 10:30
Category: Projects
Summary: Sharing our Student Support Spotlight Dashboard with the K-12 Tableau User Group


## Student Support Spotlight
In the wake of COVID19, we needed to provide [our schools](www.kippnorcal.org) with a way to identify students who would most benefit from additional supports to access distance learning. 

My colleague, [Tvisi Ravi](https://tvisig.github.io/) and I [presented](https://usergroups.tableau.com/virtualk12tugjan) our approach to developing this tool in partnership with our school teams and provided a demo of how the tool can be used. Lastly, we gave an overview of the impact it has had in our schools so far. 

I've preset the video below to begin when we started presenting, but the prior demo from [Boulder Valley School District](https://www.bvsd.org/) is also worth a watch!

<p style="text-align:center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/QiJOiDGmVpg?controls=0&amp;start=2814" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen align="middle"></iframe>
</p>

## Using Demo Data
One technique we used in order to easily prepare our student data for a public audience was to obfuscate our student names and alias our school names to quickly make this data anonymous without having to build a tool in parallel or have to duplicate the underlying data source with completely fake data. 

To accomplish this we used two approaches, in our underlying student data in [Schoolzilla](https://www.renaissance.com/products/schoolzilla/) there is a `ScrambledName` field we swapped our actual student names with. Secondly, we used Tableau's aliasing feature to rename our schools and published the alternate report to our Tableau server as a "Demo Version". 

This has also been useful internally for developing screencast tutorials without needing to expose any sensitive student information to the viewers of those tutorials. 