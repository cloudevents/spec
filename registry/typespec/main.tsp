import "@typespec/http";
import "@typespec/rest";
import "@typespec/openapi3";

using TypeSpec.Http;
using TypeSpec.Rest;

@service({
    title: "xregistry",
    description: "First pass of the xregistry api",
    version: "0.0.1",
    termsOfService: "https://github.com/cloudevents/",
    contact: {
      name: "Mark Weitzel et al.",
      url: "https://github.com/cloudevents/spec/blob/main/registry/spec.md"
    }
  })
@server("https://xregistry.example/", "Actual server to be set during client setup")
@route("/")
namespace xregistry;

@error
@doc("Error response")
model Error {
    @doc("A server-defined code that uniquely identifies the error.")
    code: string;
    @doc("Top-level error object")
    error: ErrorDetail;
}

@doc("Error details")
model ErrorDetail {
  @doc("A server-defined code that uniquely identifies the error.")
  code: string;
  @doc("A human-readable representation of the error.")
  message: string;
  @doc("An array of details about specific errors that led to this reported error.")
  details?: ErrorDetail[];
}

model Patch<T> {
  @header contentType: "application/merge-patch+json";
  ...T;
}

model List<T> {
  @doc("List of elements")
  value: T[];
  @doc("A link to the next page of results if present.")
  nextLink?: url;
}

model RegistryTag {
    key: string;
    value: string;
}

model CommonMetadata {
    singlular: string;
    plural: string;
    schema?: url;
    resources?:[CommonMetadata]
}

model RegistryMetadata {
    registryMetadata:{
      name: string;
      description: string;
      tags: RegistryTag[];
      groups:[CommonMetadata];
    }
}



model RegistryResource {
    @path
    id: string;
    name?: string;
    description?: string;
    tags?: RegistryTag[];
    version?: int32;
    epoch?: int64;
    self?: url;
    createdBy?: string;
    createdOn?: zonedDateTime;
    modifiedBy?: string;
    modifiedOn?: zonedDateTime;
    docs?: string;
}

// model a group of resources
model Group {
 @path 
 id:string;
 resources: RegistryResource[];
}

// Interfaces 
interface RegistryItemsInterface<T, P = {}> {
  @get list(...P): List<T> | Error;
  @get read(...P, @path id: string): T | Error;
  @put create(...P, @body body: T): T | Error;
  @patch update(...P, @body body: Patch<T>): T | Error;
  @delete delete(...P, @path id: string): void | Error;
}

@route("/groups")
@tag("Groups")
interface Groups extends RegistryItemsInterface<Group> {
}

//Define a "local" model here to make the interface more modular & resuable
model GroupPathId { @path groupId: string }

@route("groups/{groupId}/resources/")
@tag("Resources")
interface Resources extends RegistryItemsInterface<RegistryResource, GroupPathId> {
}

@route("/registryMetdata")
interface RegistryMetadataInterface {
  @get read(): RegistryMetadata | Error;
}