import { writable, derived } from "svelte/store";


export const friends = (() => {
  const { subscribe, set, update } = writable({});

  async function addFriend(user_id, user) {
    update(storage => {
      storage[user_id] = user;
      return storage;
    });
  }

  return { subscribe, set, addFriend };
})();


// True if friend list has not  been initialised yet
export const friendsNeedInit = derived(
  friends,
  $friends => Object.keys($friends).length === 0
);


export const initFriends = async () => {
  const url = `https://localhost:8443/api/user/friends`;
  try {
    const response = await fetch(url);
    const { friends: friendList } = await response.json();
    // TODO(high)(SpeedFox198): continue here

    if (!response.ok) {
      throw new Error(message);
    }
  
    user = { username, avatar };
    allUsers.addUser(user, user_id);

  } catch (error) {
    console.error(error);
    // TODO(low)(SpeedFox198): if default not there anymore change the default pic to something else
    user = { username:"<error>", avatar:"/default.png" };
  }
}
