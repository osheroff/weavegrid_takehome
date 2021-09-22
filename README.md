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
	contents: "Hi everybody."
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




