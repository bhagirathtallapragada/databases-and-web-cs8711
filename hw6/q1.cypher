match (e:Employee)<-[r:manages]-(d) where d.name='Research' return distinct e.fname as firstname, e.minit as middleinitial, e.lname as lastname, e.address as address