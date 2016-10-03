# Welcome to OpenWish



welcome to the OpenWish documentation page. 



## What's OpenWish?



Are you looking for an idea for your next project?

One of the best ways to do so is to see what other people want.

That's the goal behind OpenWish - to exchange wishes, needs and ideas.



## How to Get Started 



### Developers



Wan't to help out? Thanks - a helping hand is always needed.

To do so, you can do the following:



1. Improve the [core server](https://github.com/bgnalm/openWish)

2. Improve the the OpenWish client android app (the development hasn't started yet)

3. Create your own OpenWish client (Check the **API Documentation** page)



### Users



For now, the *How It Works* page is the most you can do.

Although when the first client application will be ready, your use will be a crucial part in the success of OpenWish




# How It Works



As stated before, the goal of OpenWish is wish sharing. 

In the OpenWish API, each user has basically two calls:



1. Adding a wish - a user can add a wish to the DB

2. Reading a wish - a user can read anothers user's wish

3. Rating a wish - a user can rate a wish that was read



There are two limitations:



1. Wish Reading - A user can only read as many wishes as s/he has added

This is meant to encourage wish adding

2. Wish Adding - A user's abillity to add wishes is limited by the ratings he receives on his wishes

This is meant to limit spam wishes



## How it will be implemented in the android app



The android app will have a quick "add & read" feeling: 

A user will only be able to add wishes, and every time he does so, 

he'll receive a wish - so the app will have a short "reward loop" from adding wishes,

and won't used as an analytics tool


#api

## Create User



adds a new user

accessible with */create_user* path



### Description

Required Fields:



1. user_name : the user the is adding the wish



### example

example request:

```

{

	"user_name" : "JohnDoe123",

}



```



response:

```

{

	"message" : "success",

	"data" : {

		"user_id" : "57eeab86ad775f586cd"

	},

	"success" : true

}

```


## Add Wish



adds a wish to the server.

accessible with */add_wish* path



### Description

Required Fields:



1. user_name : the user the is adding the wish



2. wish: an object describing the wish



3. wish.text - each wish has to have text





Optional Fields:



1. wish.optional : all the optional metadata about the wish



### example

example request:

```

{

	"user_name" : "JohnDoe123",

	"wish" : {

		"text" : "I wish i could know where traffic jams are going to be",

		"optional" : {

			"city" : "London",

			"recurring" : true,

			"age" : 30

		}

	}

}



```



response:

```

{

	"message" : "success",

	"data" : {

		"wish_id" : "57eeab86775f586cd"

	},

	"success" : true

}

```


## Get Wishes



retrives all the wishes the user can get

accessible with */get_wishes* path



### Description

Required Fields:



1. user_name : the user the is adding the wish



Optional Fields:



1. created_wishes : get the created wish of the user

2. read_wishes: get the wishes read by the user



if none of these are specified, both are assumed true



### example

example request:

```

{

	"user_name" : "JohnDoe123",

	"created_wishes" : true,

	"read_wishes" : true

}



```



response:

```

{

	"message" : "success",

	"data" : {

		"created_wishes" : [

			"11292523abcde",

			"6756b76abbcef123"

		],

		"read_wishes" : [

			"2234234234bdd"

		]

	},

	"success" : true

}

```


## Get Wish



retrives a wish from the server

accessible with */get_wish* path



This call is only for getting wishes that are already accessible to the user



i.e wishes that were read by the user or created by the user



###  Request Description

Required Fields:



1. user_name : the user that is getting the wish



2. wish_id: the id of the wish



### Response Description



the response data field will contain the information about the wish



### example

example request:

```

{

	"user_name" : "JohnDoe123",

	"wish_id" : "364929ed87c807a8079f"

}



```



response:

```

{

	"message" : "success",

	"data" : {

		"text" : "I wish there were more clocks",

		"time_added" : 1474535225234.

		"user_name" : "DoeJohn321",

		"rating" : 1.1,

		"number_of_reads" : 52,

		"optiona" : {

			"coountry" : "France"

		}

	},

	"success" : true

}

```


## Rate Wish



Rate a wish

accessible with */rate_wish* path



### Description

Required Fields:



1. user_name : the user the is adding the wish

2. wish_id : the wish to rate

3. rating : the rating to give (1-5)



### example

example request:

```

{

	"user_name" : "JohnDoe123",

	"wish_id" : "1133223523b234d",

	"rating" : 4.1

}



```



response:

```

{

	"message" : "success",	

	"success" : true

}

```


## Read Wish



Reads a wish. 

accessible with */read_wish* path



### Description

Required Fields:



1. user_name : the user the is adding the wish



Optional Fields:

(In development):



1. In text: read a wish with the text field that contains these words

2. field : read a wish that has a specific field

3. field value: read a wish that has a specific field value



if none of these are specified, both are assumed true



### example

example request:

```

{

	"user_name" : "JohnDoe123",

}



```



response:

```

{

	"message" : "success",

	{

	"message" : "success",

	"data" : {

		"text" : "I wish there were more clocks",

		"time_added" : 1474535225234.

		"user_name" : "DoeJohn321",

		"rating" : 1.1,

		"number_of_reads" : 52,

		"optiona" : {

			"coountry" : "France"

		}

	},

	"success" : true

}

	"success" : true

}

```


## Time Left



Gets in how much time the user will be able to do stuff

accessible with */time_left* path



### Description

Required Fields:



1. user_name : the user the is adding the wish

### example

example request:

```

{

	"user_name" : "JohnDoe123",

}



```



response:

```

{

	"message" : "success",

	"data" : {

		"can_read" : true,

		"can_post" : false,

		"next_post" : 34 (Seconds!)

	},

	"success" : true

}

```

