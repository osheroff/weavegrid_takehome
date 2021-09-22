# WeaveGrid take-home test


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
	jontents: "Hi everybody."
}
```

key reference:

- *type*: file type.  [directory, link, file]
- *path*: file path, relative to server root
- *permissions*: file permissions in octal
- *user*: file owner
- *group*: file group
- *entries*: if type is "directory", list of entries underneath
- *contents*: when type is "file", text file contentx
- *link*: when type is "link", path to file relative to server root



## Decisions made

- went with flask for route/parameter parsing as well as testability

- thought ahead of time about preventing GET "/../../../../../etc/passwd" style attacks, flask seems
  to prevent this for us by resolving the paths before us.

- Decided to resolve uid/gid to strings -- giving back numeric ids felt like leaking private data

- considered returning a directory's entries as a map instead of a list.  returning it as a list
  of hashes felt more orthogonal to the API strucutre, but I'm not 100% sure of this decision.

- Ideally the app would allow a commandline flag to allow following of symlinks outside the root folder,
  but I figured that this would add more complexity/increase code review time on your end un-necessarily.

## notes
- the basics of the app were finished in about 2 hours.  I'd say 90 minutes of that was coding and
  another 30 was yak shaving / framework wrangling.
- adding symlink support took another 45 or so.  Lots of goofy details in there, tricky to get right.
