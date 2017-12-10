#!/usr/bin/env python3

import json
import sys

import graphene

class PlaylistTracks(graphene.ObjectType):
    href = graphene.String()
    total = graphene.Int()

class Playlist(graphene.ObjectType):

    id = graphene.NonNull(graphene.String)
    name = graphene.NonNull(graphene.String)
    snapshot_id = graphene.String()
    href = graphene.String()

    tracks = graphene.Field(PlaylistTracks)

    def __init__(self, *args, **kwargs):
        super(Playlist, self).__init__(*args, **kwargs)

class Query(graphene.ObjectType):
    playlists = graphene.List(Playlist, name=graphene.String())
    playlist = graphene.Field(Playlist, id=graphene.String())

    def resolve_playlists(self, info, name):
        print(info.operation.selection_set)

        data = info.context
        if name:
            data = (entry for entry in data if entry.get("name") == name)

        print("Resolving playlists: {name: %s}" % (name))
        return [Playlist(**playlist) for playlist in data]

    def resolve_playlist(self, info, id):
        for playlist in info.context:
            if playlist.get("id") == id:
                return Playlist(**playlist)

schema = graphene.Schema(query=Query)

if __name__ == "__main__" and len(sys.argv) > 1:
    data = []
    with open("playlists.json", "r") as data_file:
        data = json.load(data_file)

    result = schema.execute(sys.argv[1], context_value=data)
    if result.errors:
        for error in result.errors:
            print(error)
    else:
        json.dump(result.data, sys.stdout, indent=2)
    print()

