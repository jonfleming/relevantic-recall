import { classifyText, sentenceClassification } from "./llm.js";
import { createClient } from "@supabase/supabase-js";
import "dotenv/config";

const supabaseUrl = process.env.VITE_SUPABASE_URL;
const supabaseAnonKey = process.env.VITE_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseAnonKey);
const userConversationCache = new Map(); // Maps user_item_id to user conversation item
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';

const client = postgres(supabaseUrl);
export const db = drizzle({ client });

export async function sendConfirmation(email) {
   try {
    const { error } = await supabase.auth.resend({
      type: "signup",
      email: email,
    });

    if (error) {
      return { error: error.message };
    }
    
    return { message: "Confirmation email resent successfully" };
  } catch (err) {
    console.error("Resend confirmation error:", err);
    return { error: err };
  }
}

export async function redirect(token) {
  try {
    // Exchange the tokens received from the email confirmation
    const { error } = await supabase.auth.verifyOtp({
      token_hash: token,
      type: "email"
    });

    if (error) {
      console.error("Auth verification error:", error);
      return { error: error.message };
    }

    // Redirect to the main application after successful verification
    return { redirect: "/?verified=true" };
  } catch (err) {
    console.error("Auth error:", err);
    return{ error: err };
  }
}

export async function saveItem(item) {
  if (item.role === "user") {
    item.classification_id = await classifyText(item);
    userConversationCache.set(item.item_id, item);
  } else {
    if (item.input_item_id) {
      const userItem = userConversationCache.get(item.input_item_id);
      item.classification_id = userItem?.classification_id + 2;
      userConversationCache.delete(item.input_item_id);
    }  
  }

  console.log("Conversation item:", item);
  const { data, error } = await supabase
    .from("conversation_items")
    .insert([item]);

  return { classification: sentenceClassification[item.classification_id], data, error };
}

export async function similaritySearch(embeddings, user) {
  const { data: contextData, error: contextError } = await supabase
    .rpc("match_conversation_items", {
      match_count: 3,
      match_threshold: 0.8,
      query_embeddings: embeddings});

  return {data: contextData, error: contextError};
}