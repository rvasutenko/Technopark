#	﻿CRUD друзей: 
**CREATE - Генерация токена быстрого приглашения:** url – <https://steamcommunity.com/invites/ajaxcreate>, нужна кука steamLoginSecure, в ответ приходит новый токен быстрого приглашения.

	{
		"invite\_token": "hrqdnrqd",
		"invite\_limit": "1",
		"invite\_duration": "2591890",
		"time\_created": 1733177401,
		"valid": 1
	}
**READ - Получение токена быстрого приглашения:** url - <https://steamcommunity.com/invites/ajaxgetall?sessionid>={id} sessionid в аргументе совпадает с значением куки sessionid в ответ на данный запрос приходит список когда-либо созданнных пользователем токенов быстрого приглашения, нужна кука steamLoginSecure.
**UPDATE - Ответ на запрос в друзья:** с кукой steamLoginSecure, POST запрос, тело:

	{
		sessionid: "d29731c20c424effacace4e8",
		steamid: "76561198868899919", // твой id
		ajax: "1",
		action: "accept",
		steamids[]: "76561198838163977" // id профиля на чей запрос отвечаем*
	}
url - <https://steamcommunity.com/profiles/>[{id}/friends/actio]()
тело ответа: 

	{
		success":1,
		"rgCounts":{
			"cFriendsPending":0,
			"cFriendsBlocked":4,
			"cFollowing":0,
			"cGroupsPending":0,
			"cFriends":37,
			"cGroups":0,
			"success":1
		}
	}
**DELETE – Удаление из друзей:** url – <https://steamcommunity.com/actions/RemoveFriendAjax>, нужна всё та же кука, тело запроса:

	{
		sessionID:	"d29731c20c424effacace4e8"
		steamid:	"76561199478984887" // id профиля друга*
	}
Тело ответа:

	true/false – успех операции
#	CRUD профиль:
**CREATE – Оставить комментарий:** url – <https://steamcommunity.com/comment/Profile/post/>{profile-id}/-1/, POST запрос, куки steamLoginSecure, тело запроса: 

	{
		comment: "..."
		count: "6"
		sessionid: "d29731c20c424effacace4e8"
		feature2: "-1"
	}
тело ответа:

	{
		success: **true**
		name	: "Profile\_76561198868899919"
		start: 0
		pagesize: "6"
		total\_count: 3
		upvotes: 0
		has\_upvoted: 0
		comments\_html: "<comment-html>"
		timelastpost: 1733182966
	}
**READ – Получение списка эмодзи:** url – <https://steamcommunity.com/actions/EmoticonList>, метод GET, нужна кука steamLoginSecure, тело запроса – пустое, тело ответа:

	{
		0: ":androxusgun:"
		1: ":toqueTLD:"
		2: ":steambored:"
		3: ":steamfacepalm:"
		4: ":steamhappy:"
		5: ":steammocking:"
		6: ":steamsad:"
		7: ":steamsalty:"
		8: ":steamthis:"
		9: ":steamthumbsdown:"
		10: ":steamthumbsup:"
	}
**UPDATE -  Изменить профиль:** url – <https://steamcommunity.com/profiles/>{profile-id}/edit/, POST запрос, нужен куки steamLoginSecure, тело запроса:

	<БОЛЬШОЕ ТЕЛО С ПЕРЕЧИСЛЕНИЕМ ВСЕХ ИЗМЕНЕНИЙ>
тело ответа:

	{
		success: 1
		errmsg: "" // сообщение об ошибке
	}
**DELETE – Удалить комментарий:** url – <https://steamcommunity.com/comment/Profile/delete/>{profile-id}/-1/, нужна кука, тело запроса:

	{
		gidcomment: "4625855867810543439"
		start: "0"
		count: "6"
		sessionid: "d29731c20c424effacace4e8"
		feature2: "-1"
	}
тело ответа: аналогично пункту **CREATE**

