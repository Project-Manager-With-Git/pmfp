
ServiceSource = """${package}
import (
	"fmt"
	"net"
	"os"
	"os/signal"
	"strings"
	"sync"
	"syscall"
	"time"

	log "github.com/Golang-Tools/loggerhelper"

	"github.com/liyue201/grpc-lb/common"
	"github.com/liyue201/grpc-lb/registry"
	zk "github.com/liyue201/grpc-lb/registry/zookeeper"

	grpc "google.golang.org/grpc"
	"google.golang.org/grpc/metadata"
)

//Server grpc的服务器结构体
type Server struct {
	AppName                            string   `json:"app_name,omitempty"`
	AppVersion                         string   `json:"app_version,omitempty"`
	Address                            string   `json:"address,omitempty"`
	LogLevel                           string   `json:"log_level,omitempty"`
	ZookeeperURL                       []string `json:"zookeeper_url,omitempty"`
	BalanceWeight                      string   `json:"balance_weight,omitempty"`

	service   *registry.ServiceInfo
	registrar *zk.Registrar
}

//Schema 参数的校验信息
func (s *Server) Schema() string {
	schema := `{
		"description": "server config",
		"type": "object",
		"required": [ "address","log_level"],
		"additionalProperties": false,
		"properties": {
			"app_name":{
				"type": "string",
				"description": "服务名"
			},
			"app_version":{
				"type": "string",
				"description": "服务版本"
			},
			"address": {
				"type": "string",
				"description": "服务的主机和端口"
			},
			"log_level":{
				"type": "string",
				"enum": ["TRACE","DEBUG","INFO","WARN","ERROR"],
				"description": "项目的log等级"
			},
			"zookeeper_url":{
				"type":"array",
				"items":{
					"type": "string"
				},
				"description": "负载均衡使用的zookeeper地址序列,以逗号分隔"
			},
			"balance_weight":{
				"type": "string",
				"description": "负载均衡的权重"
			}
		}
	}`
	return schema
}

//Main 服务的入口函数
func (s *Server) Main() {
	// 初始化log
	log.Init(s.LogLevel, log.Dict{
		"app_name":    s.AppName,
		"app_version": s.AppVersion,
	})
	log.Info("获得参数", nil, log.Dict{"ServiceConfig": s}, nil)
	s.Run()
}

//RunServer 启动服务
func (s *Server) RunServer() {
	lis, err := net.Listen("tcp", s.Address)
	if err != nil {
		log.Error("Failed to Listen", log.Dict{"error": err, "address": s.Address})
		os.Exit(1)
	}
	log.Info("Server Start", log.Dict{"address": s.Address})
	gs := grpc.NewServer()
	defer gs.Stop()
	${registservice}(gs, s)
	err = gs.Serve(lis)
	if err != nil {
		log.Error("Failed to Serve", log.Dict{"error": err})
		os.Exit(1)
	}
}

//RegistService 注册服务到zookeeper
func (s *Server) RegistService() {
	if s.registrar != nil && s.service != nil {
		log.Warn("服务注册已经初始化")
		return
	}
	port := strings.Split(s.Address, ":")[1]
	addrs, err := net.InterfaceAddrs()

	if err != nil {
		log.Error("获取本地ip失败", log.Dict{"place": "RegistService", "err": err})
		os.Exit(1)
	}
	ip := ""
	for _, _ip := range addrs {
		IP := _ip.String()
		if strings.HasPrefix(IP, "172.16.1.") {
			if strings.Contains(IP, "/") {
				ip = strings.Split(IP, "/")[0]
			} else {
				ip = IP
			}
			break
		}
	}
	if ip == "" {
		log.Error("未找到ip", log.Dict{"place": "RegistService"})
		os.Exit(1)
	}
	hostname, err := os.Hostname()
	if err != nil {
		log.Error("获取本地容器hostname失败", log.Dict{"place": "RegistService", "err": err})
		os.Exit(1)
	}
	service := &registry.ServiceInfo{
		InstanceId: hostname,
		Name:       s.AppName,
		Version:    s.AppVersion,
		Address:    fmt.Sprintf("%s:%s", ip, port),
		Metadata:   metadata.Pairs(common.WeightKey, s.BalanceWeight),
	}
	log.Info("注册的服务", log.Dict{"service": *service})
	registrar, err := zk.NewRegistrar(
		&zk.Config{
			ZkServers:      s.ZookeeperURL,
			RegistryDir:    "/backend/services",
			SessionTimeout: time.Second,
		})
	if err != nil {
		log.Error("regist error", log.Dict{"err": err})
		os.Exit(1)
	}
	s.registrar = registrar
	s.service = service

}

//Run 执行grpc服务
func (s *Server) Run() {
	if len(s.ZookeeperURL) == 0 || s.ZookeeperURL == nil {
		s.RunServer()
	} else {
		s.RegistService()
		wg := sync.WaitGroup{}
		wg.Add(1)
		go func() {
			s.RunServer()
			wg.Done()
		}()

		wg.Add(1)
		go func() {
			s.registrar.Register(s.service)
			wg.Done()
		}()
		signalChan := make(chan os.Signal, 1)
		signal.Notify(signalChan, syscall.SIGINT, syscall.SIGTERM)
		<-signalChan
		s.registrar.Unregister(s.service)
		// serv.Stop()
		wg.Wait()
	}
}

"""

HanddlerSource = """${package}
import (
	"context"

)
//Example 方法实现模板
func (s *Server) Example (ctx context.Context, in *Query) (*Response, error) {
    return &Response{}, nil
}

"""

LocalresolverSource = """${package}
import (
	resolver "google.golang.org/grpc/resolver"
)

// exampleResolver is a
// Resolver(https://godoc.org/google.golang.org/grpc/resolver#Resolver).
type localResolver struct {
	target     resolver.Target
	cc         resolver.ClientConn
	addrsStore map[string][]string
}

func (r *localResolver) start() {
	addrStrs := r.addrsStore[r.target.Endpoint]
	addrs := make([]resolver.Address, len(addrStrs))
	for i, s := range addrStrs {
		addrs[i] = resolver.Address{Addr: s}
	}
	r.cc.UpdateState(resolver.State{Addresses: addrs})
}
func (*localResolver) ResolveNow(o resolver.ResolveNowOptions) {}
func (*localResolver) Close()                                  {}

"""

SDKSource = """${package}
import (
	"errors"
	"fmt"

	log "github.com/Golang-Tools/loggerhelper"
	"github.com/liyue201/grpc-lb/balancer"
	registry "github.com/liyue201/grpc-lb/registry/zookeeper"
	grpc "google.golang.org/grpc"
	resolver "google.golang.org/grpc/resolver"
)

//SDKConfig 的客户端类型
type SDKConfig struct {
	Address              []string `json:"address"`
	BalanceWithZookeeper bool     `json:"balance_with_zookeeper,omitempty"`
	AppName              string   `json:"app_name,omitempty"`
	AppVersion           string   `json:"app_version,omitempty"`
}

//SDK 的客户端类型
type SDK struct {
	*SDKConfig
	${registclient}
	conn *grpc.ClientConn
}

//New 创建客户端对象
func New() *SDK {
	c := new(SDK)
	return c
}

//Init 初始化sdk客户端
func (c *SDK) Init(conf *SDKConfig) error {
	c.SDKConfig = conf
	if conf.Address == nil {
		return errors.New("必须至少有一个地址")
	}
	switch len(conf.Address) {
	case 0:
		{
			return errors.New("必须至少有一个地址")
		}
	case 1:
		{
			if conf.BalanceWithZookeeper {
				c.initWithZooKeeperBalance()
			} else {
				c.initStandalone()
			}
		}
	default:
		{
			if conf.BalanceWithZookeeper {
				c.initWithZooKeeperBalance()
			} else {
				c.initWithLocalBalance()
			}
		}
	}
	return nil
}

//InitStandalone 初始化客户端对象
func (c *SDK) initStandalone() error {
	conn, err := grpc.Dial(c.Address[0], grpc.WithInsecure())
	if err != nil {
		return err
	}
	c.conn = conn
	c.${registclient} = ${registclient_new}(conn)
	return nil
}

//Build 构造本地负载均衡
func (c *SDK) Build(target resolver.Target, cc resolver.ClientConn, opts resolver.BuildOptions) (resolver.Resolver, error) {
	r := &localResolver{
		target: target,
		cc:     cc,
		addrsStore: map[string][]string{
			fmt.Sprintf("%s-%s", c.AppName, c.AppVersion): c.Address,
		},
	}
	r.start()
	return r, nil
}

//Scheme 构造本地schema
func (c *SDK) Scheme() string { return "localbalancer" }

//RegistToResolver 将服务注册到resolver
func (c *SDK) RegistToResolver() {
	resolver.Register(c)
}

//InitWithLocalBalance 创建带负载均衡的客户端对象
func (c *SDK) initWithLocalBalance() error {
	Address := fmt.Sprintf("localbalancer:///%s", fmt.Sprintf("%s-%s", c.AppName, c.AppVersion))
	c.RegistToResolver()
	conn, err := grpc.Dial(Address, grpc.WithBalancerName("round_robin"), grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		return err
	}
	c.conn = conn
	c.${registclient} = ${registclient_new}(conn)
	return nil
}

//InitWithZooKeeperBalance 创建带zookeeper负载均衡的客户端对象
func (c *SDK) initWithZooKeeperBalance() error {
	registry.RegisterResolver("zk", c.Address, "/backend/services", c.AppName, c.AppVersion)
	conn, err := grpc.Dial("zk:///", grpc.WithInsecure(), grpc.WithBalancerName(balancer.RoundRobin))
	if err != nil {
		return err
	}
	log.Info("grpc dial ok", log.Dict{
		"addr": c.Address,
	})
	c.conn = conn
	c.${registclient} = ${registclient_new}(conn)
	return nil
}

//Close 断开连接
func (c *SDK) Close() error {
	return c.conn.Close()
}

//DefaultClient 默认的sdk客户端
var DefaultClient = New()

"""