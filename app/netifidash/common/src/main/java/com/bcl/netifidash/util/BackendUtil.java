package com.bcl.netifidash.util;

import com.codename1.components.ToastBar;
import com.codename1.io.*;
import com.codename1.io.rest.Response;
import com.codename1.io.rest.Rest;
import com.codename1.ui.Dialog;
import com.codename1.util.OnComplete;
import com.google.gson.Gson;


import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;

public class BackendUtil {

    public BackendUtil (){}

    public void connect(String nd_ip, String nd_port, String ip, String port, String user, String pass){
        //  Block of code to try
        String baseURL = "http://"+nd_ip+":"+nd_port+"/login";

        makePostRequest(baseURL, port, ip, user, pass);

    }

    public void makePostRequest(String url, String port, String ip, String username, String password) {

        try {

            // Create a ConnectionRequest for a POST method
            ConnectionRequest request = new ConnectionRequest() {
                @Override
                protected void readResponse(InputStream input) throws IOException {
                    super.readResponse(input);
                    Dialog.show("UniFi Connection Status", input.toString(), "OK", null);
                }

                @Override
                protected void handleErrorResponseCode(int code, String message) {
                    // Handle error here
                    Dialog.show("Error", "Error code: " + code + "\nMessage: " + message, "OK", null);
                }
            };

            request.setUrl(url);
            request.setPost(true); // Indicates this is a POST request
            request.setContentType("application/json");

            // Prepare the JSON body
            Map<String, Object> jsonBody = new HashMap<>();
            jsonBody.put("port", port);
            jsonBody.put("ip", ip);
            jsonBody.put("username", username);
            jsonBody.put("password", password);

            // Convert the map to JSON string
            String json = toJson(jsonBody);

            // Set the request body
            request.setRequestBody(json);

            // Add request headers if necessary (e.g., Authorization)
            request.addRequestHeader("Accept", "application/json");

            // Send the request
            NetworkManager.getInstance().addToQueueAndWait(request);

            if(request.getResponseCode() == 200){

                Map<String,Object> result = new JSONParser().parseJSON(new InputStreamReader(new ByteArrayInputStream(request.getResponseData()), "UTF-8"));


                Dialog.show("UniFi Connection Success", result.toString(), "OK", null);

            }

        } catch (Exception e) {

            Dialog.show("Error", "Error code: " + e.toString(), "OK", null);

            throw new RuntimeException(e);
        }

    }

    // Utility function to convert a map to a JSON string
    private String toJson(Map<String, Object> map) {
        StringBuilder jsonBuilder = new StringBuilder("{");
        boolean first = true;
        for (Map.Entry<String, Object> entry : map.entrySet()) {
            if (!first) {
                jsonBuilder.append(",");
            }
            jsonBuilder.append("\"").append(entry.getKey()).append("\":\"").append(entry.getValue()).append("\"");
            first = false;
        }
        jsonBuilder.append("}");
        return jsonBuilder.toString();
    }







}
