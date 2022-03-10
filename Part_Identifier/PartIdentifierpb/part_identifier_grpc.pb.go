// Code generated by protoc-gen-go-grpc. DO NOT EDIT.

package PartIdentifierpb

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.32.0 or later.
const _ = grpc.SupportPackageIsVersion7

// PartIdentifierServiceClient is the client API for PartIdentifierService service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type PartIdentifierServiceClient interface {
	IdentifyPart(ctx context.Context, in *IdentifyPartRequest, opts ...grpc.CallOption) (*IdentifyPartResponse, error)
}

type partIdentifierServiceClient struct {
	cc grpc.ClientConnInterface
}

func NewPartIdentifierServiceClient(cc grpc.ClientConnInterface) PartIdentifierServiceClient {
	return &partIdentifierServiceClient{cc}
}

func (c *partIdentifierServiceClient) IdentifyPart(ctx context.Context, in *IdentifyPartRequest, opts ...grpc.CallOption) (*IdentifyPartResponse, error) {
	out := new(IdentifyPartResponse)
	err := c.cc.Invoke(ctx, "/Part_Identifier.PartIdentifierService/IdentifyPart", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// PartIdentifierServiceServer is the server API for PartIdentifierService service.
// All implementations must embed UnimplementedPartIdentifierServiceServer
// for forward compatibility
type PartIdentifierServiceServer interface {
	IdentifyPart(context.Context, *IdentifyPartRequest) (*IdentifyPartResponse, error)
	mustEmbedUnimplementedPartIdentifierServiceServer()
}

// UnimplementedPartIdentifierServiceServer must be embedded to have forward compatible implementations.
type UnimplementedPartIdentifierServiceServer struct {
}

func (UnimplementedPartIdentifierServiceServer) IdentifyPart(context.Context, *IdentifyPartRequest) (*IdentifyPartResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method IdentifyPart not implemented")
}
func (UnimplementedPartIdentifierServiceServer) mustEmbedUnimplementedPartIdentifierServiceServer() {}

// UnsafePartIdentifierServiceServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to PartIdentifierServiceServer will
// result in compilation errors.
type UnsafePartIdentifierServiceServer interface {
	mustEmbedUnimplementedPartIdentifierServiceServer()
}

func RegisterPartIdentifierServiceServer(s grpc.ServiceRegistrar, srv PartIdentifierServiceServer) {
	s.RegisterService(&PartIdentifierService_ServiceDesc, srv)
}

func _PartIdentifierService_IdentifyPart_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(IdentifyPartRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(PartIdentifierServiceServer).IdentifyPart(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/Part_Identifier.PartIdentifierService/IdentifyPart",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(PartIdentifierServiceServer).IdentifyPart(ctx, req.(*IdentifyPartRequest))
	}
	return interceptor(ctx, in, info, handler)
}

// PartIdentifierService_ServiceDesc is the grpc.ServiceDesc for PartIdentifierService service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var PartIdentifierService_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "Part_Identifier.PartIdentifierService",
	HandlerType: (*PartIdentifierServiceServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "IdentifyPart",
			Handler:    _PartIdentifierService_IdentifyPart_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "Part_Identifier/PartIdentifierpb/part_identifier.proto",
}