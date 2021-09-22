# WeaveGrid take-home test

## quickstart

```
docker run -p 5000:5000 osheroff/weavegrid_takehome
curl http://localhost:5000
curl http://localhost:5000/hi_weavegrid
curl http://localhost:5000/subdir
curl http://localhost:5000?recurse=1
```

### or

```
docker run -p 5000:5000 -v $HOME:/webroot osheroff/weavegrid_takehome
curl http://localhost:5000
```

### or

```
docker run -p 5000:5000 -v $HOME:/other osheroff/weavegrid_takehome ./app.py /other
curl http://localhost:5000
```

## api reference

GET /
```
{
	type: "directory",
	path: "/",
	permissions: 755,
	user: "ben",
	group: "staff",
	entries: [
		{ path: "/src", type: "directory", permissions: 755, user: "ben", "group: "wheel" },
		{ path: "/txtfile", type: "file", permissions: 600, user: "ben", "group: "staff" }
	]
}
```

GET /txtfile
```
{
	type: "directory",
	path: "/txtfile",
	permissions: 600,
	user: "ben",
	group: "staff",
	contents: "Hi everybody.",
	size: 123
}
```

GET /symlinky
```
{
	type: "link",
	path: "/symlink",
	permissions: 600,
	user: "ben",
	group: "staff",
	link: "/link_destination"
}
```

key reference:

- *type*: file type.  [directory, link, file]
- *path*: file path, relative to server root
- *permissions*: file permissions in octal
- *user*: file owner
- *group*: file group
- *entries*: if type is "directory", list of entries underneath
- *contents*: when type is "file", text file contents
- *size*: when type is "file", size of file
- *link*: when type is "link", path to file relative to server root



## Decisions made

- went with flask for route/parameter parsing as well as testability

- thought ahead of time about preventing GET "/../../../../../etc/passwd" style attacks, flask seems
  to prevent this for us by resolving the paths before us.

- Decided to resolve uid/gid to strings -- giving back numeric ids felt like leaking private data

- considered returning a directory's entries as a map instead of a list.  returning it as a list
  of hashes felt more orthogonal to the API strucutre, but I'm not 100% sure of this decision.

- Ideally the app would allow a commandline flag to allow following of symlinks outside the root folder,
  but I figured that this would add more complexity/increase code review time unnecessarily.

- as extra credit I chose to do symlink handling and recursion

- in the interest of time I stuck with higher level functional/integration style testing, rather than module-level unit tests.
  Test coverage should nevertheless be very high.

## notes
- the basics of the app were finished in about 2 hours.  I'd say 90 minutes of that was coding and
  another 30 was yak shaving / framework wrangling.
- adding symlink support took another 45 minutes or so.  Lots of goofy details in there, tricky to get right.
- another 1.5 hours of documentation, final testing, dockerization, adding in recursion.
- took a break at the 4 hour mark.
- returned for another 30 minutes or so of code cleanup/documentation
