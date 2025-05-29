import typing as t


class NavItemProps(t.TypedDict):
    label: str
    icon: str
    href: t.Optional[str] = None
    link: t.Optional[str] = None
