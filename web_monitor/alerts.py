# -- coding: utf-8 --
items = {
	"lbc-voitures" : { 
		"url" : "http://www.leboncoin.fr/voitures/offres/rhone_alpes/?f=a&th=1&ps=9&pe=15&rs=2008&fu=1", 
		"site_handler" : "lbc_handler.LeBonCoinHandler",
		"description" : "New Voitures Rhone Alpes",
		"receivers" : ["me",],
		"notification_item" : "new_ads",
	},
	"lbc-apparts" : {
                "url" : "http://www.leboncoin.fr/locations/offres/rhone_alpes/isere/?f=a&th=1&mrs=400&mre=650&sqs=5&roe=3&ret=2&location=Grenoble%2038000%2CGrenoble%2038100",
                "site_handler" : "lbc_handler.LeBonCoinHandler",
                "description" : "Location Apparts Grenoble",
                "receivers" : ["me",],
                "notification_item" : "new_ads",
        },
}
