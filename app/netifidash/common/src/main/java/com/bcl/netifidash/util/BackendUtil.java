package com.bcl.netifidash.util;

import com.codename1.components.ToastBar;
import com.codename1.io.rest.Response;
import com.codename1.io.rest.Rest;

import java.util.Map;

public class BackendUtil {
    public BackendUtil (){

    }

    public void auth(String username, String pass){

        Response<Map> result = Rest.post("https://api.twilio.com/2010-04-01/Accounts/" + accountSID + "/Messages.json").
                queryParam("To", destinationPhone).
                queryParam("From", fromPhone).
                queryParam("Body", "Hello World").basicAuth(accountSID, authToken).getAsJsonMap();


        if(result.getResponseData() != null) {
            String error = (String)result.getResponseData().get("error_message");
            if(error != null) {
                ToastBar.showErrorMessage(error);
            }
        } else {
            ToastBar.showErrorMessage("Error sending SMS: " + result.getResponseCode());
        }

    }
}
